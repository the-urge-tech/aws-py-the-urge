import unittest
import logging

from aws_py_the_urge.util.path_manager import split_path

LOG = logging.getLogger(__name__)


class TestPathManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPathManager, cls).setUpClass()

    def test_1(self):
        path = "format=original/retailer_code=au-gucci/year=2019/month=1/day=4/39744_3417821_mp.xml.gz"
        directory, filename = split_path(path)
        LOG.debug("directory: {}".format(directory))
        LOG.debug("filename: {}".format(filename))
        self.assertEqual(
            directory,
            "format=original/retailer_code=au-gucci/year=2019/month=1/day=4")
        self.assertEqual(filename, "39744_3417821_mp.xml.gz")

    def test_2(self):
        path = "format=original/retailer_code=au-gucci/year=2019/month=1/day=4/"
        directory, filename = split_path(path)
        LOG.debug("directory: {}".format(directory))
        LOG.debug("filename: {}".format(filename))
        self.assertEqual(
            directory,
            "format=original/retailer_code=au-gucci/year=2019/month=1/day=4")
        self.assertEqual(filename, "")
