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
            "type%3Dfetched/retailer_code%3Dau-ssense/year%3D2018/month%3D10/day%3D5/crawl_id%3D20181005212630__au-ssense/20181005212630__au-ssense--fetched--j9icejmp.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(
            er.object_key,
            "type=fetched/retailer_code=au-ssense/year=2018/month=10/day=5/crawl_id=20181005212630__au-ssense/20181005212630__au-ssense--fetched--j9icejmp.jl.gz"
        )
        self.assertEqual(er.key_id, "j9icejmp")
        self.assertEqual(er.retailer_code, "au-ssense")

    def test_extract_key_id_fetched(self):
        er = EventRecord(
            bucket_name="test1",
            object_key=
            "type%3Dfetched/retailer_code%3Dau-ssense/.../20181005212630__au-ssense--fetched--j9icejmp.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(er.key_id, "j9icejmp")

    def test_extract_key_id_parsed(self):
        er = EventRecord(
            bucket_name="test1",
            object_key=
            "type%3Dparsed/retailer_code%3Dau-ssense/.../20181005212630__au-ssense--parsed--j9icejmp.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(er.key_id, "j9icejmp")

    def test_extract_key_id_enriched(self):
        er = EventRecord(
            bucket_name="test1",
            object_key=
            "type%3Denriched/retailer_code%3Dau-ssense/.../20181005212630__au-ssense--enriched--j9icejmp.jl.gz",
            event_name="ObjectCreated:Put")

        self.assertEqual(er.key_id, "j9icejmp")
