import unittest
import logging
from datetime import date, datetime
from aws_py_the_urge.util.tempfile import tempfile_crawlid_extractor

LOG = logging.getLogger(__name__)


class TestTempfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestTempfile, cls).setUpClass()

    def test_tempfile_cralid_extractor1(self):
        crawl_id = tempfile_crawlid_extractor(
            "20210526201725__enau-adidas--fetched_v2.0--_dh_oanh.jl.gz"
        )
        expected = "enau-adidas"
        self.assertEqual(crawl_id, expected)

    def test_tempfile_cralid_extractor2(self):
        crawl_id = tempfile_crawlid_extractor(
            "20210526201725__enau-adidas--business--fetched_v2.0--_dh_oanh.jl.gz"
        )
        expected = "enau-adidas--business"
        self.assertEqual(crawl_id, expected)

    def test_tempfile_cralid_extractor3(self):
        crawl_id = tempfile_crawlid_extractor(
            "/test/20210526201725__enau-adidas--business--fetched_v2.0--_dh_oanh.jl.gz"
        )
        expected = "enau-adidas--business"
        self.assertEqual(crawl_id, expected)

    def test_tempfile_cralid_extractor4(self):
        crawl_id = tempfile_crawlid_extractor(
            "/test/20210526201725__enau-adidas--business--fetched_v2.0--_dh_oanh"
        )
        expected = "enau-adidas--business"
        self.assertEqual(crawl_id, expected)
