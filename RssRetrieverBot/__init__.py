import datetime
import time
import feedparser
import logging  # loggerにしたい。
import os
import json
from typing import NamedTuple

import azure.functions as func

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(slack_token)


class Article(NamedTuple):
    article_id: int
    url: str
    title: str
    summary: str
    updated: time.struct_time


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
    list_updated: list[time.struct_time] = list(map(lambda e: e['updated_parsed'], entries))
    list_ids: list[int] = [i + 1 for i in range(len(list_titles))]
    articles_zipped = zip(list_ids, list_urls, list_titles, list_summaries, list_updated)
    return articles_zipped


def generate_section_block(text: str) -> dict:
    return {"type": "context","elements": [{"type": "plain_text", "text": text}]}


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    fabcross_rss2 = feedparser.parse('https://fabcross.jp/rss.xml')
    entries = fabcross_rss2['entries']
    list_titles = list(map(lambda e: e['title'], entries))
    list_dicts = list(
        map(lambda e: {'url': e['link'], 'title': e['summary']}, entries))

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    try:
        blocks = [generate_section_block(txt) for txt in list_titles]
        response = client.chat_postMessage(
            channel=os.environ["channel_id"],
            text="rss bot titles",
            blocks=blocks
        )
        client.chat_postMessage(
            channel=os.environ["channel_id"],
            text=str(list_dicts),
            thread_ts=response['message']['ts']
        )

        logging.info('Slack Messaging API response is %s', str(response))
    except SlackApiError as e:
        logging.info('Slack Api Error %s', str(e))
        assert e.response['error']
