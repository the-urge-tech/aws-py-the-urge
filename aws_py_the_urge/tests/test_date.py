import unittest
import logging
from datetime import date, datetime
from aws_py_the_urge.lib.s3_manager.file_manager import FileS3
from aws_py_the_urge.util.date import get_newest_file, path_date_extractor

LOG = logging.getLogger(__name__)


class TestPathManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPathManager, cls).setUpClass()

    def test_path_date_extractor(self):
        date_extr = path_date_extractor(
            "format=original/retailer_code=au-gucci/year=2018/month=10/day=4/39744_3417821_mp.xml.gz"
        )
        expected = date(2018, 10, 4)
        self.assertEqual(date_extr, expected)

        date_extr = path_date_extractor(
            "format=original/year=2018/month=1/day=11/xxxx/xxx/39744_3417821_mp.xml.gz"
        )
        expected = date(2018, 1, 11)
        self.assertEqual(date_extr, expected)

        date_extr = path_date_extractor(
            "format=original/retailer_code=au-gucci/year=2000/month=3/day=22/file.file"
        )
        expected = date(2000, 3, 22)
        self.assertEqual(date_extr, expected)

    def test_1(self):
        list_path = [
            FileS3(
                key=
                'type=fetched/retailer_code=au-gucci/year=2019/month=2/day=12/crawl_id=20190212202406__au-gucci/20190212202406__au-gucci--fetched_v2.0--i8m868o9.jl.gz',
                last_modify=datetime(2019, 2, 12, 9, 24, 58),
                meta={}),
            FileS3(
                key=
                'type=fetched/retailer_code=au-gucci/year=2019/month=2/day=7/crawl_id=20190207151857__au-gucci/20190207151857__au-gucci--fetched_v2.0--clgdi084.jl.gz',
                last_modify=datetime(2019, 2, 7, 4, 20, 34),
                meta={}),
            FileS3(
                key=
                'type=fetched/retailer_code=au-gucci/year=2019/month=2/day=8/crawl_id=20190207151857__au-gucci/20190207151857__au-gucci--fetched_v2.0--f7vimbre.jl.gz',
                last_modify=datetime(2019, 2, 7, 4, 19, 51),
                meta={})
        ]

        newest_file = get_newest_file(list_path, '.gz')
        LOG.debug("newest_file: {}".format(newest_file))
        self.assertEqual(
            newest_file,
            "type=fetched/retailer_code=au-gucci/year=2019/month=2/day=12/crawl_id=20190212202406__au-gucci/20190212202406__au-gucci--fetched_v2.0--i8m868o9.jl.gz"
        )

    def test_no_gz_files(self):
        list_path = [
            FileS3(
                key=
                'type=fetched/retailer_code=au-gucci/year=2019/month=2/day=12/crawl_id=20190212202406__au-gucci/None',
                last_modify=datetime(2019, 2, 12, 9, 24, 58),
                meta={}),
            FileS3(
                key=
                'type=fetched/retailer_code=au-gucci/year=2019/month=2/day=7/crawl_id=20190207151857__au-gucci/20190207151857__au-gucci--fetched_v2.0--clgdi084.jl',
                last_modify=datetime(2019, 2, 7, 4, 20, 34),
                meta={}),
            FileS3(
                key=
                'type=fetched/retailer_code=au-gucci/year=2019/month=2/day=8/crawl_id=20190207151857__au-gucci/',
                last_modify=datetime(2019, 2, 7, 4, 19, 51),
                meta={})
        ]

        newest_file = get_newest_file(list_path, '.gz')
        LOG.debug("newest_file: {}".format(newest_file))
        self.assertEqual(newest_file, None)
