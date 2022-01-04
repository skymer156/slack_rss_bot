import feedparser
import pprint


fabcross_rss2 = feedparser.parse('https://fabcross.jp/rss.xml')
pprint.pprint(fabcross_rss2, depth=1)

entries = fabcross_rss2['entries']
list_dicts = list(
    map(lambda e: {'url': e['link'], 'title': e['summary']}, entries))
# pprint.pprint(list_summaries)

list_titles = list(map(lambda e: e['title'], entries))
pprint.pprint(list_titles)
