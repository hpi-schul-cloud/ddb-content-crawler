import argparse

from crawler.crawler import DeutscheDigitaleBibliothekCrawler
from src import settings
from src.api import BildungsserverFeed, LocalXmlFeed, LocalRssFeed
from src.crawler import Crawler, SiemensCrawler, BildungsserverCrawler
from src.exceptions import ConfigurationError

if __name__ == '__main__':
    crawler = DeutscheDigitaleBibliothekCrawler()
    crawler.crawl()
