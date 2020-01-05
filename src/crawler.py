import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ["https://www.semanticscholar.org/paper/Tackling-Climate-Change-with-Machine-Learning-Rolnick-Donti/998039a4876edc440e0cabb0bc42239b0eb29644"]
    
    def parse(self, response):
        print("********************")
        title = response.css('#paper-header h1 ::text').extract_first()
        abstract = response.css('.abstract__text::text').extract_first()
        date = response.css('.paper-meta li:nth-child(2) span:nth-child(2) ::text').extract_first()
        authors = response.css('.author-list span a ::text').extract()
        references = response.css('#references .card-content .paper-detail-content-card .citation-list__citations .paper-citation .citation__body h2 a span span ::text').extract()
        references_links = response.css('#references .card-content .paper-detail-content-card .citation-list__citations .paper-citation .citation__body h2 a ::attr(href)').extract()
        yield{
            'title': title,
            'abstract': abstract,
            'date' : date,
            'authors' : authors,
            'references' : references,
            'references_links' : references_links
        }