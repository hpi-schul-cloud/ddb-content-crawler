from threading import Thread

from abc import ABC, abstractmethod

import requests
import json
import settings


class SourceFeed(ABC):
    base_url = settings.SOURCE_LOCATION

    @abstractmethod
    def get_feed(self) -> dict:
        ...


def get_media_url(type_id):
    return 'https://api.deutsche-digitale-bibliothek.de/search?query=*&facet=type_fct&type_fct=mediatype_00{}'.format(
        type_id)


def get_sparte_url(type_id):
    return 'https://api.deutsche-digitale-bibliothek.de/search?query=*&facet=type_fct&type_fct=mediatype_00{}'.format(
        type_id)


def get_item_view(item_id):
    return 'https://api.deutsche-digitale-bibliothek.de/items/{id}/view'.format(id=item_id)


def get_item_edm(item_id):
    return 'https://api.deutsche-digitale-bibliothek.de/items/{id}/edm'.format(id=item_id)


class DeutscheDigitaleBibliothekFeed(SourceFeed):
    @property
    def offset(self):
        return self.page * self.page_size

    page_size = 10

    def __init__(self):
        self.page = 0
        self.max_result = 9999999999
        self.check_sizes()

    def check_sizes(self):
        r = requests.get(self.base_url, params={'rows': 1},
                         headers=self.headers)
        if r.ok:
            response_dict = r.json()
            print('all %i' % (response_dict['numberOfResults'],))
        acc = 0
        for i in range(10):
            r = requests.get(get_media_url(i), params={'rows': 1},
                             headers=self.headers)
            if r.ok:
                response_dict = r.json()
                acc += response_dict['numberOfResults']
                print('media_type00{} {} '.format(i, response_dict['numberOfResults']))
                try:
                    print(response_dict['results'][0]['docs'][0]['media'])
                except IndexError:
                    pass
                print(acc)

    # https://api.deutsche-digitale-bibliothek.de/doku/display/ADD/search#search-Request4
    # https://api.deutsche-digitale-bibliothek.de/doku/display/ADD/Medientyp
    def get_feed(self) -> dict:
        while self.offset <= self.max_result:
            r = requests.get(self.base_url, params={'offset': self.offset, 'rows': self.page_size},
                             headers=self.headers)
            if r.ok:
                self.page += 1

                response_dict = r.json()
                print(response_dict)
                self.max_result = response_dict['numberOfResults']
                for item in response_dict['results'][0]['docs']:
                    # todo schedule item ids
                    yield item
            else:
                raise ConnectionRefusedError(
                    'The Feed could not be established: status:{} {}'.format(r.status_code, r.content))

    @property
    def headers(self):
        return {
            'Accept': 'application/json',
            'Host': 'api.deutsche-digitale-bibliothek.de',
            'Authorization': 'OAuth oauth_consumer_key="{}"'.format(settings.API_KEY)
        }


class FeedWorkerThread(Thread):
    pass


class LocalJsonFeed(SourceFeed):

    def get_feed(self) -> dict:
        with open(self.base_url, mode="r", encoding="utf-8") as f:
            content = json.load(f)
        return content['results'][0]['docs']
