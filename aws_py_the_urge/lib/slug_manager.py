from slugify import Slugify
from aws_py_the_urge.resources.resource_loader import load_slug_rule
import logging

LOG = logging.getLogger(__name__)


class SlugManager(object):
    def __init__(
        self, language, product_name=None, color=None, brand=None, fingerprint=None
    ):
        self.language = language
        self.field_dict = {
            "product_name": product_name,
            "color": color,
            "brand": brand,
            "fingerprint": fingerprint,
        }

    def keyword_list_lookup(self):
        orders = {
            "fr": ["product_name", "brand", "color"],
            "it": ["product_name", "brand", "color"],
            "es": ["product_name", "brand", "color"],
            "en": ["color", "brand", "product_name"],
            "ja": ["color", "brand", "product_name"],
            "ko": ["color", "brand", "product_name"],
            "ar": ["color", "brand", "product_name"],
            "de": ["color", "brand", "product_name"],
            "ru": ["product_name", "color", "brand"],
            "pt": ["product_name", "color", "brand"],
            "zh": ["color", "brand", "product_name"],
            "zh-hans": ["product_name", "color", "brand"],
        }
        return [self.field_dict.get(i, None) for i in orders.get(self.language, [])]

    def slugify(self):
        if (
            self.field_dict["product_name"] is not None
            and self.field_dict["brand"] is not None
            and self.field_dict["fingerprint"] is not None
        ):
            key_word_list = self.keyword_list_lookup()
            pretranslate = load_slug_rule(self.language)
            slugify_url = Slugify(pretranslate=pretranslate)
            slugify_url.to_lower = True
            slugify_url.stop_words = ()
            slugify_url.max_length = 1000
            first_bit = slugify_url(
                "-".join(key_word for key_word in key_word_list if key_word).lower(),
                max_length=1000,
            )
            if len(first_bit) == 0:
                return ""

            friendly_id = "-".join([first_bit, self.field_dict["fingerprint"]])
            return friendly_id

    def slugify_brand(self):
        return self.slugify_field("brand")

    def slugify_fingerprint(self):
        return self.slugify_field("fingerprint")

    def slugify_field(self, field_name):
        pretranslate = load_slug_rule(self.language)
        slugify_url = Slugify(pretranslate=pretranslate)
        slugify_url.to_lower = True
        slugify_url.stop_words = ()
        slugify_url.max_length = 1000
        return slugify_url(self.field_dict[field_name], max_length=1000)
