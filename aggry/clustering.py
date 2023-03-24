import os
import sqlite3
import numpy as np

import unicodedata
from janome.tokenizer import Tokenizer
from sklearn.cluster import DBSCAN
from scipy.sparse import lil_matrix


connection = sqlite3.connect('db.sqlite3')
c = connection.cursor()

# IDのリストとタイトルのリストを作成
c.execute('''
            SELECT id, title, mod_location FROM aggry_app_jobs
                ''')
result = c.fetchall()
result = [list(r) for r in result] # タプルをリストに変換
input_strings = []
input_ids = []
for r in result:
    r[1] = r[1].strip().replace('/', '').replace('|', '').replace('【ConMa(コンマ)】', '') # 機械学習用にタイトルを整形
    if r[2] in r[1]: # 勤務地の文字列を含む場合はその文字列を除外
        r[1] = r[1].replace(r[2], '')
    input_strings.append(r[1])
    input_ids.append(r[0])

# 各文字列をUnicode正規化して、janomeでわかちがきにする
tokenizer = Tokenizer() # janomeトークナイザーの初期化
tokenized_strings = []
for string in input_strings:
    # Unicode正規化
    normalized_string = unicodedata.normalize("NFKC", string)
    # janomeでわかちがきにする
    tokens = tokenizer.tokenize(normalized_string)
    tokenized_strings.append([token.surface for token in tokens])

# 単語リストを作成
words = set()
for string in tokenized_strings:
    for token in string:
        words.add(token)
word_list = list(words)
word_list.sort()

# データ行列を作成
data_matrix = lil_matrix((len(input_strings), len(word_list)), dtype=np.int32)
for i, string in enumerate(tokenized_strings): # タイトルを一つずつループ
    for num, token in enumerate(string): # わかちがきした単語を一つずつループ
        j = word_list.index(token)
        data_matrix[i, j] += 1
        if token == "工事": # 工事という単語があれば、その前と前の前の文字列に重みをつける
            j1 = word_list.index(string[num-1])
            j2 = word_list.index(string[num-2])
            data_matrix[i, j1] += 1
            data_matrix[i, j2] += 2
            

# DBSCANクラスタリングを実行
dbscan = DBSCAN(eps=1.5, min_samples=2) # ep=1.5~3が良い？。1.5だと150個くらいに分割される。
dbscan.fit(data_matrix.toarray())

# ID,タイトル、ラベルを格納したリストを作成
labeling_list = []
for i, label in enumerate(dbscan.labels_):
    labeling_list.append([input_ids[i], input_strings[i], label])
    

# １レコードずつラベルを入れる
for l in labeling_list:            
    # プレースホルダーを使ったSQL文を作成する
    sql = "update aggry_app_jobs set label1 = ? where id = ?"
    # プレースホルダーに渡す変数をタプルで指定する
    params = (int(l[2]),l[0])
    # SQL文を実行する
    c.execute(sql, params)
    
    connection.commit()        

connection.close()

print("クラスタリング終了")