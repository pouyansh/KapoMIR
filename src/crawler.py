import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ["https://www.semanticscholar.org/paper/Tackling-Climate-Change-with-Machine-Learning-Rolnick-Donti/998039a4876edc440e0cabb0bc42239b0eb29644"]
    crawl_urls = ["https://www.semanticscholar.org/paper/Tackling-Climate-Change-with-Machine-Learning-Rolnick-Donti/998039a4876edc440e0cabb0bc42239b0eb29644", "https://www.semanticscholar.org/paper/Sublinear-Algorithms-for-(%CE%94%2B-1)-Vertex-Coloring-Assadi-Chen/eb4e84b8a65a21efa904b6c30ed9555278077dd3", "https://www.semanticscholar.org/paper/Processing-Data-Where-It-Makes-Sense%3A-Enabling-Mutlu-Ghose/4f17bd15a6f86730ac2207167ccf36ec9e6c2391"]
    paper_id = 0
    def parse(self, response):
        title = response.css('#paper-header h1 ::text').extract_first()
        abstract = response.xpath("//meta[@name='description']/@content")[0].extract()
        date = response.css('.paper-meta li:nth-child(2) span:nth-child(2) ::text').extract_first()
        authors = response.xpath("//meta[@name='citation_author']/@content").extract()
        references = response.css('#references .card-content .paper-detail-content-card .citation-list__citations .paper-citation .citation__body h2 a span span ::text').extract()
        references_links = response.css('#references .card-content .paper-detail-content-card .citation-list__citations .paper-citation .citation__body h2 a ::attr(href)').extract()
        for i in references_links[:5]:
            if i in self.crawl_urls:
                    continue
            url = "https://www.semanticscholar.org" + i
            self.crawl_urls.append(i)
        
        references_ids = []        
        for i in references_links:
            references_ids.append(i[-40:])
        yield{
            'id' : self.crawl_urls[self.paper_id][-40:],
            'title': title,
            'abstract': abstract,
            'date' : date,
            'authors' : authors,
            'references' : references_ids,
            'references_names' : references
        }
        
        self.paper_id += 1
        next_page = self.crawl_urls[self.paper_id]
        
        if self.paper_id <= 5500 :
            yield response.follow(next_page, callback = self.parse)