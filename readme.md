# RSSを用いたSlack Botアプリケーション

テストではfabcrossのrssを使わさせていただいています。

## 使用している技術

* Python3.9
* Azure Functions (TimerTrigger)
* Slack API
* RSS2.0

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

tools

* autopep8
* flake8
* venv

## 今後変更内容

* feedparserから取得するデータから全角を消す。
* feedparserのレスポンスに問題がないか確認して、問題があればエラーコードをSlackに通知
* loggingをloggerに変える
* rssから取得したデータをBlockkitに組み込む。
* Google Spreadsheet APIを使用して、updateの値を保存＋前回の確認を行い、新しいデータのみを取り出す処理を入れる。
* 全体的な処理における構造のチェックと関数化を行う。
* postMessage関数のモジュール化
* 各種マジックナンバーのconfig化(os.environに入れるもの、config.iniに入れるもので分ける。
* Blockkitのデータをjsonに入れ、フォルダを作成してそこに入れる。
* 投稿するメッセージに番号を振る
* メッセージの分割を行う。
* 他のRSSでどうなるのかを調べたい。
* RSS自体の詳細というか、引用元を記載したい。
* 可能であればSlack APIのmodelsの使い方を知りたい。
* Google Spread Sheetではなく、Azure Storageを使用したい。
* typingの追加
* 今後追加予定のメソッド、クラスにテストコードの付与
