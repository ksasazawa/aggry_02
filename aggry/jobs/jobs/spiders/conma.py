import scrapy
from jobs.conma_item import Jobs
from scrapy.loader import ItemLoader
import datetime


class ConmaSpider(scrapy.Spider):
    name = "conma"
    allowed_domains = ["conma.jp"]
    start_urls = ["https://conma.jp/zenkoku/PC13/MC1", "https://conma.jp/zenkoku/PC13/MC2"]
    # "https://conma.jp/zenkoku/PC13/MC5,6"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        rows = response.css("table#w0 tr")
        for i, r in enumerate(rows.extract()):
            if '<th>職種</th>' in r:
                job_no = i+1
            elif '<th>勤務地</th>' in r:
                location_no = i+1
            elif '<th>給与</th>' in r:
                price_no = i+1
            elif '<th>仕事内容</th>' in r:
                detail_no = i+1
            elif '<th>待遇/福利厚生</th>' in r:
                welfare_no = i+1
        loader = ItemLoader(item=Jobs(), response=response)
        loader.add_css('title', 'h1.resultTitle::text')
        if "電気" in response.css(f'table#w0 tr:nth-child({job_no})>td::text').get() or "設備" in response.css(f'table#w0 tr:nth-child({job_no})>td::text').get():
            # hensu = response.css(f'table#w0 tr:nth-child({job_no})>td::text').get()
            # print(f"職種はifで{hensu}")
            loader.add_value('job', "設備施工管理")
        else:
            # hensu = response.css(f'table#w0 tr:nth-child({job_no})>td::text').get()
            # print(f"職種はelseで{hensu}")
            loader.add_css('job', f'table#w0 tr:nth-child({job_no})>td::text')
        loader.add_css('location', f'table#w0 tr:nth-child({location_no})>td::text')
        loader.add_css('price', f'table#w0 tr:nth-child({price_no})>td::text')
        
        # 仕事内容のtdを取得し、不要な文字列を削除
        detail_all = response.css(f'table#w0 tr:nth-child({detail_no})>td').get()
        detail_all = ''.join(detail_all.split()).replace('''''', '').replace('<td>', '').replace('</td>', '').replace('<br>', '\n')
        loader.add_value('detail', detail_all)
        
        # 福利厚生のtdを取得し、不要な文字列を削除
        welfare_all = response.css(f'table#w0 tr:nth-child({welfare_no})>td').get()
        welfare_all = ''.join(welfare_all.split()).replace('''''', '').replace('<td>', '').replace('</td>', '').replace('<br>', '\n')
        loader.add_value('welfare', welfare_all)
        
        loader.add_value('agent', '株式会社アーキ・ジャパン')
        loader.add_value('agent_url', 'https://akijapan.co.jp/')
        loader.add_value('url', response.request.url)
        loader.add_value('data_added', datetime.datetime.now())
        yield loader.load_item()
        


    def parse(self, response):
        job_box = response.css('div.mod-jobResultBox')
        for job in job_box:
            url = job.css('div.btn-group>div.btn-group__right.hide-sp>a::attr(href)').get()       
            yield response.follow(url=url, callback=self.parse_item)
        next_page = response.css('li.next>a::attr(href)').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
