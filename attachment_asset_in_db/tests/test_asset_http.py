# Copyright 2026 Akretion (https://www.akretion.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo.tests import HttpCase, tagged

ASSET_SRC_RE = re.compile(r'src="(/web/assets/[^"]+\.js)"')


@tagged("post_install", "-at_install")
class TestAssetHttp(HttpCase):
    def test_asset_bundle_served_from_db(self):
        """Browse the login page like a user would, then fetch its JS bundles:
        they must be served directly (HTTP 200) from `db_datas`, not
        redirected to their own URL (infinite redirect loop since v20.0).
        """
        response = self.url_open("/web/login")
        self.assertEqual(response.status_code, 200)
        asset_urls = ASSET_SRC_RE.findall(response.text)
        self.assertTrue(asset_urls, "No JS asset bundle found in /web/login")

        for url in asset_urls:
            with self.subTest(url=url):
                attachment = self.env["ir.attachment"].search(
                    [("url", "=", url)], limit=1
                )
                self.assertTrue(attachment.db_datas)
                self.assertFalse(attachment.store_fname)

                response = self.url_open(url, allow_redirects=False)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content, attachment.raw.content)

    def test_asset_stream_type(self):
        """Low-level check: a db-stored attachment having a URL is streamed
        as data, not as a redirection to its URL."""
        attachment = self.env["ir.attachment"].create(
            {
                "name": "foo.min.js",
                "mimetype": "application/javascript",
                "raw": b"console.log('foo');",
                "url": "/web/assets/123abcd/foo.min.js",
                "public": True,
            }
        )
        self.assertTrue(attachment.db_datas)
        stream = attachment._to_http_stream()
        self.assertEqual(stream.type, "data")
        self.assertEqual(stream.data, b"console.log('foo');")
