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
    # todo query params "offset = 21 & rows = 2 & sort
    # todo only digitized?
    # https: // api.deutsche - digitale - bibliothek.de / doku / display / ADD / search  # search-Request4
    # https: // api.deutsche - digitale - bibliothek.de / doku / display / ADD / Medientyp
    def get_feed(self) -> dict:
        r = requests.get(self.base_url, headers=self.headers)
        return r.json()['results']

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

