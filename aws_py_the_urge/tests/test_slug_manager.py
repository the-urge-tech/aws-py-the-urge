import unittest
import logging

from aws_py_the_urge.lib.slug_manager import SlugManager

LOG = logging.getLogger(__name__)


class TestSlugManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestSlugManager, cls).setUpClass()

    def test_en(self):
        result = SlugManager(
            "en",
            product_name="A Product Name",
            brand="A GREAT Brand",
            color="Black",
            fingerprint="123-ss",
        ).slugify()
        expected = "black-great-brand-product-name-123-ss"
        self.assertEqual(expected, result)

    def test_language_does_not_exist(self):
        result = SlugManager(
            "AAAAAAAA",
            product_name="A Product Name",
            brand="A GREAT Brand",
            color="Black",
            fingerprint="123-ss",
        ).slugify()
        expected = ""
        self.assertEqual(expected, result)

    def test_brand(self):
        result = SlugManager("en", brand="Ajeсиний").slugify_brand()
        expected = "ajesinii"
        self.assertEqual(expected, result)

    def test_language_ru(self):
        result = SlugManager(
            "ru",
            product_name="Сумка с ведром акации",
            brand="Aje",
            color="Сумеречный синий",
            fingerprint="123-ss",
        ).slugify()
        expected = "sumka-s-vedrom-akatsii-sumerechnyiy-siniy-aje-123-ss"
        self.assertEqual(expected, result)

    def test_language_ja(self):

        result = SlugManager(
            "ja",
            product_name="Overtureデニムミニスカート",
            brand="Aje",
            color="ブルーデニム",
            fingerprint="123-ss",
        ).slugify()
        expected = "burudenimu-aje-overturedenimuminisukato-123-ss"
        self.assertEqual(expected, result)
