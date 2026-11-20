# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class TestAttachment(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = b"foo"

    def _create_attachment(self, name, mimetype=None):
        vals = {"name": name, "raw": self.data}
        if mimetype:
            vals["mimetype"] = mimetype
        return self.env["ir.attachment"].create(vals)

    def test_asset_web_icon_data(self):
        attachment = self._create_attachment("web_icon_data")
        self.assertEqual(attachment.db_datas.content, b"foo")

    def test_asset_css(self):
        attachment = self._create_attachment("foo", mimetype="text/css")
        self.assertEqual(attachment.db_datas.content, b"foo")

    def test_not_asset(self):
        attachment = self._create_attachment("foo")
        self.assertFalse(attachment.db_datas)

    def test_multi_write(self):
        attachments = self._create_attachment("foo")
        attachments |= self._create_attachment("bar")
        attachments.write({"raw": self.data})
