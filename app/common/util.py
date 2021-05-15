from collections import Counter
import datetime
from bs4 import BeautifulSoup
import jieba.analyse


def tags(content):
    return jieba.analyse.extract_tags(content, topK=10, allowPOS=('n'))


def getcontent(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


def formatDatetime(time):
    d = datetime.datetime(*(time[0:6]))
    return d.isoformat(' ')


def get_tags(feed):
    contents = [
        tags(getcontent(entry.content) + entry.title) for entry in feed.entries
    ]
    tag_list = [tag for item in contents for tag in item]
    res = sorted(Counter(tag_list).items(), key=lambda x: x[1], reverse=True)
    return str([tag[0] for tag in res[:3]])