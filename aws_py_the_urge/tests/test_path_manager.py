import unittest
import logging

from aws_py_the_urge.util.path_manager import split_path, get_exension

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

    def test_extension(self):
        file_name = "name.gzip"
        extenison = get_exension(file_name)
        LOG.debug("extenison: {}".format(extenison))
        self.assertEqual(extenison, ".gzip")

    def test_extension_empty(self):
        file_name = "none"
        extenison = get_exension(file_name)
        LOG.debug("extenison: {}".format(extenison))
        self.assertEqual(extenison, "")

    def test_extension_multi(self):
        file_name = "name.csv.gzip"
        extenison = get_exension(file_name)
        LOG.debug("extenison: {}".format(extenison))
        self.assertEqual(extenison, ".gzip")

    def test_extension_path(self):
        file_name = "sub1/sub2/name.csv.gzip"
        extenison = get_exension(file_name)
        LOG.debug("extenison: {}".format(extenison))
        self.assertEqual(extenison, ".gzip")
