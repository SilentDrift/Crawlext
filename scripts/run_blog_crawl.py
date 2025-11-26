import os
import sys
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(repo_root))
    os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "crawler.settings")
    process = CrawlerProcess(get_project_settings())
    process.crawl("blog_spider")
    process.start()


if __name__ == "__main__":
    main()
