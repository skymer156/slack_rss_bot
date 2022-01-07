import datetime
import time
import feedparser
import logging  # loggerにしたい。
import os
import configparser


import azure.functions as func

from typing import NamedTuple
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(slack_token)
inifile = configparser.ConfigParser()
inifile.read("RssRetrieverBot/config.ini")


class Article(NamedTuple):
    article_id: int
    url: str
    title: str
    summary: str
    updated: time.struct_time

    def as_chaanel_block(self):
        text = f"{self.article_id} <{self.url}|記事リンク> {self.title}"
        return_dict = {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": text
                }
                    ]
            }
        return return_dict

    def as_thread_block(self):
        text = f"{self.article_id} <{self.url}|記事リンク> {self.summary}"
        return_dict = {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": text
                }
                    ]
            }
        return return_dict


def get_article_list_from_rss(rss_path: str) -> list[Article]:
    rssfeed = feedparser.parse(rss_path)
    entries: list = rssfeed['entries']
    articles_zipped = get_zipped_article_from_entries(entries)
    return list(map(lambda var: Article._make(var), articles_zipped))


def get_zipped_article_from_entries(entries: list):
    """rssフィードから取得したentriesリストの中から、
    記事のタイトル、リンク、要約、更新日、idのタプルをzip化して返す関数。
    Keyword arguments:
    argument -- entries: list
    Return: zip[tuple[int, str, str, str, time.struct_time]]
    """

    list_titles: list[str] = list(map(lambda e: e['title'], entries))
    list_urls: list[str] = list(map(lambda e: e['link'], entries))
    list_summaries: list[str] = list(map(lambda e: e['summary'], entries))
    list_updated: list[time.struct_time] = list(
        map(lambda e: e['updated_parsed'], entries))
    list_ids: list[int] = [i + 1 for i in range(len(list_titles))]
    articles_zipped = zip(list_ids, list_urls, list_titles,
                          list_summaries, list_updated)
    return articles_zipped


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    # rssのxmlから、Articleオブジェクトのリストを作成する。
    article_list = get_article_list_from_rss(inifile["DEFAULT"]["rsspath"])
    # channel用のblocksを作成する。blocksはslackの表示フォーマットに従う。
    channel_block_list = list(
        map(lambda article: article.as_chaanel_block(), article_list))
    # thread用のblocksを作成する。blocksはslackの表示フォーマットに従う。
    thread_block_list = list(
        map(lambda article: article.as_thread_block(), article_list)
    )

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    try:
        # slackの任意のチャンネルにメッセージをPOSTする。
        response = client.chat_postMessage(
            channel=os.environ["channel_id"],
            text="rss bot titles",
            blocks=channel_block_list
        )
        # 送信したメッセージにスレッドを作る形でメッセージをPOSTする。
        client.chat_postMessage(
            channel=os.environ["channel_id"],
            text="rss bot summaries",
            thread_ts=response['message']['ts'],
            blocks=thread_block_list
        )

        logging.info('Slack Messaging API response is %s', str(response))
    except SlackApiError as e:
        logging.info('Slack Api Error %s', str(e))
        assert e.response['error']
