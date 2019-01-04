import unittest
import logging

from aws_py_the_urge.util.date import get_newest_file

LOG = logging.getLogger(__name__)


class TestPathManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPathManager, cls).setUpClass()

    def test_1(self):
        list_path = [
            "format=original/retailer_code=au-gucci/year=2018/month=10/day=25/None",
            "format=original/retailer_code=au-gucci/year=2018/month=10/day=4/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=10/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=11/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=12/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=13/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=14/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=15/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=16/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=17/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=18/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=19/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=20/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=22/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=23/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=24/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=25/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=26/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=29/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=30/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=8/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=9/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=12/day=1/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=12/day=19/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=12/day=2/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=12/day=20/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=12/day=3/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=12/day=4/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2018/month=12/day=5/39744_3417821_mp.xml.gz",
            "format=original/retailer_code=au-gucci/year=2019/month=1/day=2/",
            "format=original/retailer_code=au-gucci/year=2019/month=1/day=2/39744_3417821_mp.xml.gz"
        ]

        newest_file = get_newest_file(list_path, '.gz')
        LOG.debug("newest_file: {}".format(newest_file))
        self.assertEqual(
            newest_file,
            "format=original/retailer_code=au-gucci/year=2019/month=1/day=2/39744_3417821_mp.xml.gz"
        )

    def test_no_gz_files(self):
        list_path = [
            "format=original/retailer_code=au-gucci/year=2018/month=10/day=25/None",
            "format=original/retailer_code=au-gucci/year=2018/month=10/day=4/",
            "format=original/retailer_code=au-gucci/year=2018/month=11/day=10/39744_3417821",
            "format=original/retailer_code=au-gucci/year=2019/month=1/day=2/",
            "format=original/retailer_code=au-gucci/year=2019/month=1/day=2/"
        ]

        newest_file = get_newest_file(list_path, '.gz')
        LOG.debug("newest_file: {}".format(newest_file))
        self.assertEqual(newest_file, None)
