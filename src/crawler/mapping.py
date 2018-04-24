from exceptions import MappingException

base_url = "https://www.deutsche-digitale-bibliothek.de"


def get_item_url(_, item):
    return "{}/item/{}".format(base_url, item['id'])


def build_url_from_key(key, item):
    if key in item:
        return "{}/{}".format(base_url, item[key])
    return ''


def get_description(_, item):
    return "{title} {subtitle}".format(**item)


def default_transform(key, item):
    return item[key]


class Mapping:
    def __init__(self, name: str, transform: object = default_transform) -> object:
        self.name = name
        self.transform = transform


class StaticMapping(Mapping):
    """
    Static Mapping is not useful at the moment, we initiate resource objects with static fields, if needed
    """
    def __init__(self, name: str) -> object:
        super().__init__(name)
        self.transform = lambda *_: name


class Mapper:
    target_to_source_mapping = {}

    def map_source_to_target(self, element):
        """
        target_to_source_mapping is a dict with  a simple DSL:
        all the mapping-keys of are keys of the target dict and get the source element for mapping
        1. If the value of the mapping-key is a Mapping, apply the Mapping on the element
        2. If the value of the mapping-key is a String use this key on the input-array to get the output
        3. If there the transformation is "None" just pass through the key-value of the input to the key-value of the
            output

        :param element:
        :return: dict the
        """
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
                print('no match for key {} on element {}'.format(key, element))
        return target_dict


class DDBSchulCloudMapper(Mapper):
    target_to_source_mapping = {
        "title": "title",
        "url": Mapping("id", get_item_url),
        "originId": "id",
        "description": Mapping("beschreibung", get_description),
        # "licenses": None,  # "Mapping("rechte", lambda m: [w.text for w in m]),
        "tags": "category",  # lambda m,_: [w.strip() for w in m[0].text.split(';')]),
        "thumbnail": Mapping("thumbnail", build_url_from_key),
    }
