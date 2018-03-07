import logging
from jsonschema import ValidationError

from crawler.exceptions import MappingException
from crawler.feed import DeutscheDigitaleBibliothekFeed, LocalJsonFeed
from api import ResourceSchema, ResourceAPI
from crawler.mappings import Mapping


class Crawler:
    provider_name = None
    target_to_source_mapping = None
    source_api = None

    def __init__(self, target_api=ResourceAPI) -> None:
        self.logger = logging.getLogger(self.provider_name)
        self.source_api = self.source_api()
        self.target_api = target_api()

    def log(self, message):
        self.logger.error(message)

    def crawl(self):
        feed = self.source_api.get_feed()
        for child in feed:
            resource_dict = self.parse(child)
            resource = self.validate(resource_dict)
            # if resource:
            #    self.target_api.add_resource(resource)

    def parse(self, element: dict) -> dict:
        target_dict = {}
        for key, transformation in self.target_to_source_mapping.items():
            try:
                if isinstance(transformation, Mapping):
                    target_dict[key] = transformation.transform(key, element)
                elif type(transformation) is str:
                    target_dict[key] = element[transformation]
                elif transformation is None:
                    target_dict[key] = element[key]
                else:
                    raise MappingException('mapping for key{} is invalid')
            except KeyError:
                print('no match for key {} on element {}'.format(key, element['id'], element['title']))
        return target_dict

    def validate(self, resource_dict):
        target_format = ResourceSchema(self.provider_name, **resource_dict)
        try:
            self.target_api.validate(target_format)
        except ValidationError as e:
            # self.log(e)
            return None
        return target_format


base_url = "https://www.deutsche-digitale-bibliothek.de"


def get_item_url(_, item):
    return "{}/item/{}".format(base_url, item['id'])


def get_thumbnail(key, item):
    if hasattr(item,key):
        return "{}/{}".format(base_url, item[key])
    return ''


def get_description(_, item):
    return "{title} {subtitle}".format(**item)


class DeutscheDigitaleBibliothekCrawler(Crawler):
    provider_name = "Deutsche Digitale Bibliothek"
    source_api = LocalJsonFeed  # DeutscheDigitaleBibliothekFeed

    target_to_source_mapping = {
        "title": "title",
        "url": Mapping("id", get_item_url),
        "originId": "id",
        "description": Mapping("beschreibung", get_description),
        #"licenses": None,  # "Mapping("rechte", lambda m: [w.text for w in m]),
        "mimeType": "media",
        #"contentCategory": None,
        "tags": "category",  # lambda m,_: [w.strip() for w in m[0].text.split(';')]),
        "thumbnail": Mapping("thumbnail", get_thumbnail),
        #"providerName": None,
    }
