def default_transform(key, item):
    return item[key]


class Mapping:
    def __init__(self, name: str, transform: default_transform) -> None:
        self.name = name
        self.transform = transform
