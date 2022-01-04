import datetime
import feedparser
import logging  # loggerにしたい。
import os
import json

import azure.functions as func

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(slack_token)


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    # configにしてファイル別にする。
    fabcross_rss2 = feedparser.parse('https://fabcross.jp/rss.xml')
    entries = fabcross_rss2['entries']
    list_titles = list(map(lambda e: e['title'], entries))
    list_dicts = list(
        map(lambda e: {'url': e['link'], 'title': e['summary']}, entries))
    text = '\n'.join(list_titles)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    try:
        # with open('RssRetrieverBot/sample.json', 'r') as f:
        #    dict_block = json.load(f)
        #blocks = dict_block['blocks']
        # 長くて汚いので、postMessageは関数にしてまとめておく。
        response = client.chat_postMessage(
            channel="C02022797K8",  # os.environに入れる。
            text=text  # blocks=blocks
        )
        client.chat_postMessage(
            channel="#times_seki",
            text=str(list_dicts),
            thread_ts=response['message']['ts']
        )
        # ここまで関数化。
        logging.info('Slack Messaging API response is %s', str(response))
    except SlackApiError as e:
        logging.info('Slack Api Error %s', str(e))
        assert e.response['error']
