from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sqlite3
import datetime
import os
import time
import re

# import numpy as np
# import unicodedata
# from janome.tokenizer import Tokenizer
# from sklearn.cluster import DBSCAN
# from scipy.sparse import lil_matrix


class JobsPipeline:
    def __init__(self):
        self.cnt = 0

    # 既存のデータを削除
    def open_spider(self, spider):
        # db.sqlite3と同じディレクトリに移動
        os.chdir('../')
        self.connection = sqlite3.connect('db.sqlite3')
        self.c = self.connection.cursor()
        
        if spider.name == "copro":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '株式会社コプロ・エンジニアード'
                                ''')
            
        if spider.name == "conma":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '株式会社アーキ・ジャパン'
                                ''')
            
        if spider.name == "kyodo":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '共同エンジニアリング株式会社'
                                ''')

        if spider.name == "sekokannavi":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '株式会社ウィルオブ・コンストラクション'
                                ''')

        if spider.name == "oreyume":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '株式会社夢真' and job = '建築施工管理'
                                ''')
            
        if spider.name == "oreyume2":
            self.c.execute('''
                            DELETE FROM aggry_app_jobs WHERE agent = '株式会社夢真' and job = '土木施工管理'
                                ''')
            
        self.connection.commit()



    # 勤務地を整形してlabel以外のデータを格納
    def process_item(self, item, spider):
        
        # 市区町村までを取得する関数
        def remove_postal_code(address):
            address = address.replace('　', '').replace(' ', '')
            m = re.search(r'(市|区|町|村|郡)', address[4:])
            murayama = re.search(r'村山市', address)
            # 東村山や武蔵村山への対応
            if murayama:
                index = murayama.start() + 3
                return address[:index]
            # それ以外
            elif m:
                index = m.start() + 5
                return address[:index]
            else:
                return address
        
        # 東京都という文字列を含まないか、市区町村を含まない場合抽出対象から外す。    
        if '東京都' not in item.get('location') or re.search(r'(市|区|町|村|郡)', item.get('location')) is None:
            raise DropItem("This item is not located in Tokyo")
        
        else:
            self.cnt += 1
            print(f"{self.cnt}個めのデータです！！！--------------------------------")
            self.c.execute('''
                                INSERT INTO aggry_app_jobs (title, job, location, mod_location, price, detail, welfare, agent, agent_url, url, data_added)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''',(
                                    item.get('title'),
                                    item.get('job'),
                                    item.get('location'),
                                    remove_postal_code(item.get('location')),
                                    item.get('price'),
                                    item.get('detail'),
                                    item.get('welfare'),
                                    item.get('agent'),
                                    item.get('agent_url'),
                                    item.get('url'),
                                    item.get('data_added'),
                                ))
            self.connection.commit()
            return item



    def close_spider(self, spider):       
        self.connection.close()
        
        
        
        


    