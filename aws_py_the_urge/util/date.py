import re
from datetime import date, datetime


def path_date_extractor(path):
    matches = re.search('.*?\/year=(.*)?\/month=(.*)?\/day=(.*)?\/(.*)', path)
    return date(
        int(matches.group(1)), int(matches.group(2)), int(matches.group(3)))


def crawlid_date_extractor(crawl_id):
    numbers = crawl_id.split('__')[0]
    return datetime.strptime(numbers, '%Y%m%d%H%M%S')
