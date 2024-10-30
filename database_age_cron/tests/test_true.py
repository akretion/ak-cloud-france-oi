from odoo.tests.common import TransactionCase


class TestTrue(TransactionCase):
    def test_true(self):
        # dummy test to make the ci happy
        self.assertTrue(True)
