import settings
from crawler.crawler import DeutscheDigitaleBibliothekCrawler

if __name__ == '__main__':
    dry_run = settings.DRY_RUN
    crawler = DeutscheDigitaleBibliothekCrawler(dry_run=dry_run)
    crawler.crawl()
