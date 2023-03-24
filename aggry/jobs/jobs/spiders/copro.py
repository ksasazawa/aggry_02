import scrapy
from jobs.copro_item import Jobs
from scrapy.loader import ItemLoader
import datetime


class GenCareeSpider(scrapy.Spider):
    name = "copro"
    allowed_domains = ["g-career.net"]
    start_urls = ["https://www.g-career.net/jobs/list?employment%5B%5D=1&parent_area%5B%5D=436&prefecture_area%5B%5D=013&occupation%5B%5D=2&keyword=%E6%9D%B1%E4%BA%AC",
                  "https://www.g-career.net/jobs/list?employment%5B%5D=1&parent_area%5B%5D=436&prefecture_area%5B%5D=013&occupation%5B%5D=7&keyword=%E6%9D%B1%E4%BA%AC",]
    # "https://www.g-career.net/jobs/list?employment%5B%5D=1&parent_area%5B%5D=436&prefecture_area%5B%5D=013&occupation%5B%5D=12&occupation%5B%5D=17&keyword=%E6%9D%B1%E4%BA%AC"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        loader = ItemLoader(item=Jobs(), response=response)
        loader.add_css('title', 'h1.mainTtl::text')
        if response.css('dl.jobInfo>div:nth-child(2)>dd::text').get() in ('空調衛生設備施工管理', '電気施工管理'):
            loader.add_value('job', "設備施工管理")
        else:
            loader.add_css('job', 'dl.jobInfo>div:nth-child(2)>dd::text')
        loader.add_css('job', 'dl.jobInfo>div:nth-child(2)>dd::text')
        loader.add_css('location', 'dl.jobInfo>div:nth-child(1)>dd::text')
        loader.add_css('price', 'dl.jobInfo>div:nth-child(3)>dd::text')
        
        # 仕事内容のtdを取得し、不要な文字列を削除
        detail_all = response.css('table.jobTable tr:nth-child(1)>td').get()
        detail_all = ''.join(detail_all.split()).replace('''''', '').replace('<td>', '').replace('</td>', '').replace('<br>', '\n')
        loader.add_value('detail', detail_all)
        
        # 福利厚生のtdを取得し、不要な文字列を削除
        welfare_all = response.css('table.jobTable tr:nth-child(8)>td').get()
        welfare_all = ''.join(welfare_all.split()).replace('''''', '').replace('<td>', '').replace('</td>', '').replace('<br>', '\n')
        loader.add_value('welfare', welfare_all)
        
        loader.add_value('agent', '株式会社コプロ・エンジニアード')
        loader.add_value('agent_url', 'https://www.copro-e.co.jp/')
        loader.add_value('url', response.request.url)
        loader.add_value('data_added', datetime.datetime.now())
        yield loader.load_item()


    def parse(self, response):
        job_box = response.css('div.jobWrap')
        for job in job_box:
            url = job.css('div.jobIn>a::attr(href)').get()            
            yield response.follow(url=url, callback=self.parse_item)
        next_page = response.css('div.pagerBox.pcOnly>ul.pagerItems>li.pagerItem_next>a::attr(href)').get()
        if next_page and next_page != "#":
            yield response.follow(url=next_page, callback=self.parse)
