from pathlib import Path

import scrapy

class CianSpider(scrapy.Spider):
    name = "cian"

    def start_requests(self):
        urls = [
            "https://kazan.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=4777&room1=1",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"cian-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")