import logging
from jsonschema import ValidationError

from crawler.feed import DeutscheDigitaleBibliothekFeed
from schema import ResourceSchema, ResourceAPI
from crawler.mapping import DDBSchulCloudMapper, Mapper


class Crawler:
    provider_name = None
    mapper = None
    source_api = None

    def __init__(self, mapper: Mapper, target_api=ResourceAPI, dry_run: bool=False) -> None:
        self.logger = logging.getLogger(self.provider_name)
        self.source_api = self.source_api()
        self.mapper = mapper
        self.target_api = target_api()
        self.dry_run = dry_run

    def log(self, message):
        self.logger.error(message)

    def crawl(self):
        feed = self.source_api.get_feed()
        for child in feed:
            resource_dict = self.parse(child)
            resource = self.validate(resource_dict)
            if resource and not self.dry_run:
                self.target_api.add_resource(resource)
            elif resource:
                self.log(resource)

    def parse(self, element: dict) -> dict:
        return self.mapper.map_source_to_target(element)

    def validate(self, resource_dict):
        target_format = ResourceSchema(self.provider_name, **resource_dict)
        try:
            self.target_api.validate(target_format)
        except ValidationError as e:
            self.log(e)
            return None
        return target_format


class DeutscheDigitaleBibliothekCrawler(Crawler):
    provider_name = "Deutsche Digitale Bibliothek"
    source_api = DeutscheDigitaleBibliothekFeed

    def __init__(self, *args, **kwargs):
        super().__init__(DDBSchulCloudMapper(), *args, **kwargs)
