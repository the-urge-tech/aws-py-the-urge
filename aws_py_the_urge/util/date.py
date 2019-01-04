import re
from datetime import date, datetime
import logging

LOG = logging.getLogger(__name__)


def path_date_extractor(path):
    matches = re.search('.*?\/year=(.*)?\/month=(.*)?\/day=(.*)?\/(.*)', path)
    return date(
        int(matches.group(1)), int(matches.group(2)), int(matches.group(3)))


def get_newest_file(list_path_files, extension=""):
    true_filtered_files = [obj for obj in list_path_files if extension in obj]
    if not true_filtered_files:
        return None
    list_date_files = [path_date_extractor(obj) for obj in true_filtered_files]
    LOG.debug("list_date_objects:{}".format(list_date_files))
    newest_date = max(list_date_files)
    LOG.debug("newest_date:{}".format(newest_date))
    idx_newest_date = list_date_files.index(newest_date)
    LOG.debug("idx_newest_date:{}".format(idx_newest_date))
    return true_filtered_files[idx_newest_date]


def crawlid_date_extractor(crawl_id):
    numbers = crawl_id.split('__')[0]
    return datetime.strptime(numbers, '%Y%m%d%H%M%S')
