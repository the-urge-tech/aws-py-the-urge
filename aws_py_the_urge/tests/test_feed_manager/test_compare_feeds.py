import logging
import unittest
from unittest.mock import patch

from aws_py_the_urge.lib.feed_manager import FeedManager

LOG = logging.getLogger(__name__)


def moked_s3(*args, **kwargs):
    return


def moked_get_last_feed_content(*args, **kwargs):
    return {b'test1'}


class TestComaringFeeds(unittest.TestCase):
    @patch('aws_py_the_urge.lib.s3_manager.s3_parent.S3Parent.__init__',
           side_effect=moked_s3())
    @patch(
        'aws_py_the_urge.lib.feed_manager.FeedManager.get_last_feed_content',
        side_effect=moked_get_last_feed_content())
    def test_comparing_feeds_different(self, mock1, mock2):
        retailer_code = "au-ssense"
        response_body = b"different text"
        result = FeedManager(retailer_code, "").is_equal_to_last(response_body)
        LOG.debug("result test_comparing_feeds_equal ={}".format(result))
        self.assertFalse(result)
        mock1.assert_called()
        mock2.assert_called()

    @patch('aws_py_the_urge.lib.s3_manager.s3_parent.S3Parent.__init__',
           side_effect=moked_s3())
    @patch(
        'aws_py_the_urge.lib.feed_manager.FeedManager.get_last_feed_content',
        side_effect=moked_get_last_feed_content())
    def test_comparing_feeds_equal(self, mock1, mock2):
        retailer_code = "au-ssense"
        response_body = b"test1"
        result = FeedManager(retailer_code, "").is_equal_to_last(response_body)
        LOG.debug("result test_comparing_feeds_equal ={}".format(result))
        self.assertTrue(result)
        mock1.assert_called()
        mock2.assert_called()

    @patch('aws_py_the_urge.lib.s3_manager.s3_parent.S3Parent.__init__',
           side_effect=moked_s3())
    @patch(
        'aws_py_the_urge.lib.feed_manager.FeedManager.get_last_feed_content',
        side_effect=moked_get_last_feed_content())
    def test_comparing_feeds_zip_equal(self, mock1, mock2):
        retailer_code = "au-ssense"
        with open("tests/resources/example_zip_file.txt", 'rb') as f:
            response_body = f.read()

        result = FeedManager(retailer_code,
                             "").is_equal_to_last(response_body,
                                                  binary=False,
                                                  file_extension=".zip")
        LOG.debug("result test_comparing_feeds_equal = {}".format(result))

        self.assertTrue(result)
        mock1.assert_called()
        mock2.assert_called()
