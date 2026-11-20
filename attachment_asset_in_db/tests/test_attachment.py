# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.tests import TransactionCase


class TestAttachment(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = base64.b64encode(b"foo")

    def _create_attachment(self, name, mimetype=None):
        return self.env["ir.attachment"].create(
            {
                "name": name,
                "datas": self.data,
                "mimetype": mimetype,
            }
        )

    def test_asset_web_icon_data(self):
        attachment = self._create_attachment("web_icon_data")
        self.assertEqual(attachment.db_datas, b"foo")

    def test_asset_css(self):
        attachment = self._create_attachment("foo", mimetype="text/css")
        self.assertEqual(attachment.db_datas, b"foo")

    def test_not_asset(self):
        attachment = self._create_attachment("foo")
        self.assertFalse(attachment.db_datas)

    def test_asset_scss_text_plain(self):
        # Reproduce the bug where updating a custom .scss asset changes
        # its mimetype to "text/plain": it must still be stored in the
        # database.
        attachment = self._create_attachment("foo.scss", mimetype="text/scss")
        self.assertTrue(attachment.db_datas)
        attachment.write({"datas": self.data, "mimetype": "text/plain"})
        self.assertEqual(attachment.db_datas, b"foo")

    def test_multi_write(self):
        attachments = self._create_attachment("foo")
        attachments |= self._create_attachment("bar")
        attachments.write({"datas": self.data})
