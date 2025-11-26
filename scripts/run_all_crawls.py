import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "crawler.settings")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl("arxiv_rl_spider")
    process.crawl("blog_spider")
    process.start()


if __name__ == "__main__":
    main()
