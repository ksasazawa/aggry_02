import scrapy
from jobs.oreyume_item import Jobs
from scrapy.loader import ItemLoader
import datetime


class OreyumeSpider(scrapy.Spider):
    name = "oreyume"
    allowed_domains = ["oreyume.com"]
    start_urls = ["https://www.oreyume.com/search/JB63/JS21057/PC13/EC33/"]
    # "https://www.oreyume.com/search/JB63/JS21093/PC13/EC33/", "https://www.oreyume.com/search/JB63/JS21095/PC13/EC33/"
    
    def __init__(self):
        self.page_cnt = 1
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        rows = response.css("div#unker02>table tr")
        for i, r in enumerate(rows.extract()):
            if '<th>募集職種</th>' in r:
                job_no = i+1
            elif '<th>勤務地</th>' in r:
                location_no = i+1
            elif '<th>給与待遇</th>' in r:
                price_no = i+1
            elif '<th>仕事内容</th>' in r:
                detail_no = i+1
            elif '<th>待遇･福利厚生</th>' in r:
                welfare_no = i+1
        loader = ItemLoader(item=Jobs(), response=response)
        loader.add_css('title', f'div#unker02>table tr:nth-child({job_no})>td::text')
        loader.add_css('job', f'div#unker02>table tr:nth-child({job_no})>td::text')
        loader.add_css('location', f'div#unker02>table tr:nth-child({location_no})>td::text')
        loader.add_css('price', f'div#unker02>table tr:nth-child({price_no})>td::text')
        
        # 仕事内容のtdを取得し、不要な文字列を削除
        detail_all = response.css(f'div#unker02>table tr:nth-child({detail_no})>td').get()
        detail_all = ''.join(detail_all.split()).replace('''''', '').replace('<td>', '').replace('</td>', '').replace('<br>', '\n')
        loader.add_value('detail', detail_all)
        
        # 福利厚生のtdを取得し、不要な文字列を削除
        welfare_all = response.css(f'div#unker02>table tr:nth-child({welfare_no})>td').get()
        welfare_all = ''.join(welfare_all.split()).replace('''''', '').replace('<td>', '').replace('</td>', '').replace('<br>', '\n')
        loader.add_value('welfare', welfare_all)
        
        loader.add_value('agent', '株式会社夢真')
        loader.add_value('agent_url', 'https://yumeshin.co.jp/')
        loader.add_value('url', response.request.url)
        loader.add_value('data_added', datetime.datetime.now())
        yield loader.load_item()
        

  
    def parse(self, response):
        job_box = response.css('div.card:not(.h-100)')
        for job in job_box:
            url = job.css('div.excerpt_txt_box a.todec::attr(href)').get() 
            yield response.follow(url=url, callback=self.parse_item)
        next_page = response.css('div.pager.d-none.d-md-block li.next>a::attr(href)').get()
        if next_page and next_page != f'?page={self.page_cnt}':
            print(f"{self.page_cnt}ページ目です")
            self.page_cnt += 1
            yield response.follow(url=next_page, callback=self.parse)