import unittest

from aws_py_the_urge.app import EventRecord


class EventRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(EventRecordTests, cls).setUpClass()

    def test_event_record_create(self):
        er = EventRecord(
            bucket_name="test1",
            object_key=
            "type%3Dfetched/retailer_code%3Dau-ssense/year%3D2018/month%3D10/day%3D5/crawl_id%3D20181005212630__au-ssense/20181005212630__au-ssense--fetched_v2.0--j9icejmp.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(
            er.object_key,
            "type=fetched/retailer_code=au-ssense/year=2018/month=10/day=5/crawl_id=20181005212630__au-ssense/20181005212630__au-ssense--fetched_v2.0--j9icejmp.jl.gz"
        )
        self.assertEqual(er.named_tmp_file_id, "j9icejmp")
        self.assertEqual(er.retailer_code, "au-ssense")

    def test_extract_named_tmp_file_id_fetched(self):
        er = EventRecord(
            bucket_name="test1",
            object_key=
            "type%3Dfetched/retailer_code%3Dau-ssense/.../20181005212630__au-ssense--fetched_v2.0--j9icejmp.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(er.named_tmp_file_id, "j9icejmp")

    def test_extract_named_tmp_file_id_parsed(self):
        er = EventRecord(
            bucket_name="test1",
            object_key=
            "type%3Dparsed/retailer_code%3Dau-ssense/.../20181005212630__au-ssense--parsed_v2.0--j9icejmp.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(er.named_tmp_file_id, "j9icejmp")

    def test_extract_named_tmp_file_id_enriched(self):
        er = EventRecord(
            bucket_name="test1",
            object_key=
            "type%3Denriched/retailer_code%3Dau-ssense/.../20181005212630__au-ssense--enriched_v2.0--j9icejmp.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(er.named_tmp_file_id, "j9icejmp")

    def test_extract_named_tmp_file_id_alternated(self):
        er = EventRecord(
            bucket_name="test1",
            object_key=
            "type%3Dalternated/retailer_code%3Dau-ssense/year%3D2019/month%3D3/day%3D1/crawl_id%3D20190301110826__au-ssense/20190301110826__au-ssense--alternated_v2.0--00onxyom.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(er.named_tmp_file_id, "00onxyom")

    def test_extract_named_tmp_file_id_ingested(self):
        er = EventRecord(
            bucket_name="test1",
            object_key=
            "type=ingested/retailer_code=au-camilla-and-marc/year=2019/month=5/day=17/crawl_id=20190517010856__au-camilla-and-marc/20190517010856__au-camilla-and-marc--ingested_v2.0-alternated--z0298d5o.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(er.named_tmp_file_id, "z0298d5o")

    def test_extract_named_tmp_file_id_dropped(self):
        er = EventRecord(
            bucket_name="test1",
            object_key=
            "type=dropped/retailer_code=au-bec-and-bridge/year=2019/month=5/day=17/crawl_id=20190517010849__au-bec-and-bridge/20190517010849__au-bec-and-bridge--dropped_v2.0-enriched--e3w9fvyi.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(er.named_tmp_file_id, "e3w9fvyi")