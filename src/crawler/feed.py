from abc import ABC, abstractmethod

import requests
import json
import settings


class SourceFeed(ABC):
    base_url = settings.SOURCE_LOCATION

    @abstractmethod
    def get_feed(self) -> dict:
        ...


class DeutscheDigitaleBibliothekFeed(SourceFeed):
    @property
    def offset(self):
        return self.page * self.page_size

    page_size = 10

    def __init__(self):
        self.page = 0
        self.max_result = 9999999999

    # https: // api.deutsche - digitale - bibliothek.de / doku / display / ADD / search  # search-Request4
    # https: // api.deutsche - digitale - bibliothek.de / doku / display / ADD / Medientyp
    def get_feed(self) -> dict:
        while self.offset <= self.max_result:
            r = requests.get(self.base_url, params={'offset': self.offset, 'rows': self.page_size},
                             headers=self.headers)
            self.page += 1
            response_dict = r.json()
            self.max_result = response_dict['numberOfResults']
            for item in response_dict['results'][0]['docs']:
                yield item

    @property
    def headers(self):
        return {
            'Accept': 'application/json',
            'Host': 'api.deutsche-digitale-bibliothek.de',
            'Authorization': 'OAuth oauth_consumer_key="{}"'.format(settings.API_KEY)
        }


class LocalJsonFeed(SourceFeed):

    def get_feed(self) -> dict:
        with open(self.base_url, mode="r", encoding="utf-8") as f:
            content = json.load(f)
        return content['results'][0]['docs']
