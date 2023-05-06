# Aggggry　〜派遣求人特化の2✖️アグリゲーションサイト〜

![title image](./images/aggggry2.png)

## 概要
施工管理の派遣求人主要サイトから求人情報をクローリングし、類似求人をグルーピング表示。

## 仕様
下記定期実行
- 既存データ削除
- 対象サイトをクローリング
    - コプロ
        - https://www.g-career.net/
    - アーキジャパン
        - https://conma.jp/
    - 夢真
        - https://www.oreyume.com/
- クローリングデータをDBに保存
- 求人タイトルをわかち書きにし、求人タイトル✖️単語の出現回数の行列を作成
- クラスタリングし、各求人にラベリング
- 20求人グループごとにページ分割して表示


## 技術Tips
- Replitによるデプロイ
    - Replitで管理者画面を表示する方法
        - https://replit.com/@BenBotDISCORD/laba?v=1
- DjangoによるWEBフレームワーク実装
    - 基礎
        - https://www.youtube.com/watch?v=O037g3NOoXY&t=571s
        - https://www.udemy.com/course/django-todoapp-in-5day/
    - 応用
        - https://www.udemy.com/course/python-django-web/
- scrapyによるクローリング
    - https://www.udemy.com/course/python-web-scraping-with-scrapy/
- APSchedulerによる定期実行（cronだとreplitで動作しない）
    - https://next-k.site/blog/archives/2022/07/25/847
- unicodedataとjanomeによる自然言語処理
    - https://rinsaka.com/python/hyaku/02-mecab.html
- DBScanによるクラスタリング
    - https://qiita.com/takechanman1228/items/c7f23873c087630bab18
- 画面表示
    - ページ分割
        - https://djangobrothers.com/blogs/django_pagination/
    - formのデザイン
        - https://hodalog.com/how-to-use-bootstrap-4-forms-with-django/
    - bulma CSS
        - https://johobase.com/bulma-cheat-sheet/
- アプリケーションがダウンしないようにするには
    - UptimeRobot
        - https://uptimerobot.com/dashboard

