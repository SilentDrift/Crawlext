import scrapy


class ArxivRawItem(scrapy.Item):
    source = scrapy.Field()
    query_id = scrapy.Field()
    arxiv_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    abstract = scrapy.Field()
    categories = scrapy.Field()
    submitted_at = scrapy.Field()
    updated_at = scrapy.Field()
    raw_meta = scrapy.Field()


class PaperItem(scrapy.Item):
    source = scrapy.Field()
    arxiv_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    abstract = scrapy.Field()
    categories = scrapy.Field()
    submitted_at = scrapy.Field()
    updated_at = scrapy.Field()
    rl_tags = scrapy.Field()
    attention_score = scrapy.Field()
    collected_at = scrapy.Field()


class BlogRawItem(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    published_at = scrapy.Field()
    html = scrapy.Field()
    collected_at = scrapy.Field()


class BlogPostItem(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    published_at = scrapy.Field()
    text = scrapy.Field()
    rl_tags = scrapy.Field()
    attention_score = scrapy.Field()
    collected_at = scrapy.Field()
