from datetime import datetime, date
from django.core.cache import cache
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import subprocess

def periodic_execution():
    os.chdir('jobs')

    spider_process1 = subprocess.Popen(['scrapy', 'crawl', 'oreyume2'])
    spider_process1.wait()

    spider_process2 = subprocess.Popen(['scrapy', 'crawl', 'copro'])
    spider_process2.wait()
    
    spider_process3 = subprocess.Popen(['scrapy', 'crawl', 'oreyume'])
    spider_process3.wait()
    
    spider_process4 = subprocess.Popen(['scrapy', 'crawl', 'conma'])
    spider_process4.wait()
    
    os.chdir('../')
    subprocess.Popen(['python', 'clustering.py'])


# スケジュールの設定
def start():
    scheduler=BackgroundScheduler()
    scheduler.add_job(periodic_execution, 'cron', hour=16, minute=31)
    scheduler.start()