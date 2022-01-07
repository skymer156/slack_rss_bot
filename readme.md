# RSSを用いたSlack Botアプリケーション

[fabcross様のrss](https://fabcross.jp/rss.xml)を使わさせていただいています。

## 使用上の注意

1. 環境変数を使用しているため、使用する環境に環境変数をsetすること。
2. 取得するRSSのURLをconfig.iniに記載すること。
3. ライブラリ等は、requirement.txtに記載しているため、それを元にインストールすること。

## 使用している技術

* Python3.9
* Azure Functions (TimerTrigger)
* Slack API
* RSS2.0

ブランチ構成はmain/develop/feature

## 使用Pythonパッケージ

* datetime
* feedparser
* logging
* os
* azure.functions
* slack_sdk
* json(予定)
* google cloud API(予定)
* typing, Namedtuple
* configparser

tools

* autopep8
* flake8
* venv

## 今後変更内容

* feedparserから取得するデータから全角を消す。
* feedparserのレスポンスに問題がないか確認して、問題があればエラーコードをSlackに通知
* loggingをloggerに変える
* rssから取得したデータをBlockkitに組み込む。 -> OK
* Google Spreadsheet APIを使用して、updateの値を保存＋前回の確認を行い、新しいデータのみを取り出す処理を入れる。
* 全体的な処理における構造のチェックと関数化を行う。 -> little OK
* postMessage関数のモジュール化
* 各種マジックナンバーのconfig化(os.environに入れるもの、config.iniに入れるもので分ける。 -> OK
* Blockkitのデータをjsonに入れ、フォルダを作成してそこに入れる。
* 投稿するメッセージに番号を振る -> article_idで実装。
* メッセージの分割を行う。 -> Articleクラスのリスト化で分割。
* 他のRSSでどうなるのかを調べたい。
* RSS自体の詳細というか、引用元を記載したい。 -> readmeの頭に.
* 可能であればSlack APIのmodelsの使い方を知りたい。 -> 独自のクラスに記述。公式documentにはないか。
* Google Spread Sheetではなく、Azure Storageを使用したい。
* typingの追加 -> 関数には記載。
* 今後追加予定のメソッド、クラスにテストコードの付与
