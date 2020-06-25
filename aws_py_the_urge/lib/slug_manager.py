from slugify import slugify_url

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
            "en": ["color", "brand", "product_name"],
            "fr": ["product_name", "brand", "color"],
            "it": ["product_name", "brand", "color"],
            "ja": ["color", "brand", "product_name"],
            "ko": ["color", "brand", "product_name"],
            "ru": ["product_name", "color", "brand"],
        }
        return [self.field_dict.get(i, None) for i in orders.get(self.language, [])]

    def slugify(self):
        if (
            self.field_dict["product_name"] is not None
            and self.field_dict["brand"] is not None
            and self.field_dict["fingerprint"] is not None
        ):
            key_word_list = self.keyword_list_lookup()
            first_bit = slugify_url(
                "-".join(key_word for key_word in key_word_list if key_word).lower(),
                max_length=1000,
            )
            if len(first_bit) == 0:
                return ""

            friendly_id = "-".join([first_bit, self.field_dict["fingerprint"]])
            return friendly_id
