from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPartnerSequence(TransactionCase):
    def test_partner_customer_sequence(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Test Customer",
                "is_customer": True,
            }
        )
        self.assertTrue(partner.customer_number, "Customer ID should be generated")

    def test_partner_vendor_sequence(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Test Vendor",
                "is_vendor": True,
            }
        )
        self.assertTrue(partner.vendor_number, "Vendor ID should be generated")

    def test_unique_vat(self):
        self.env["res.partner"].create(
            {
                "name": "Partner A",
                "vat": "123456789",
            }
        )
        with self.assertRaises(ValidationError):
            self.env["res.partner"].create(
                {
                    "name": "Partner B",
                    "vat": "123456789",
                }
            )

    def test_partner_employee_sequence(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Test Employee Partner",
                "is_employee": True,
            }
        )
        self.assertTrue(partner.employee_number, "Employee ID should be generated")

    def test_hr_employee_sequence(self):
        employee = self.env["hr.employee"].create(
            {
                "name": "Test HR Employee",
            }
        )
        self.assertTrue(employee.employee_number, "HR Employee ID should be generated")

    def test_partner_write(self):
        partner = self.env["res.partner"].create({"name": "Test Write Partner"})
        self.assertFalse(partner.customer_number)
        self.assertFalse(partner.vendor_number)
        self.assertFalse(partner.employee_number)

        partner.write({"is_customer": True, "is_vendor": True, "is_employee": True})

        self.assertTrue(
            partner.customer_number, "Customer ID should be generated on write"
        )
        self.assertTrue(partner.vendor_number, "Vendor ID should be generated on write")
        self.assertTrue(
            partner.employee_number, "Employee ID should be generated on write"
        )

    def test_hr_employee_with_existing_id(self):
        employee = self.env["hr.employee"].create(
            {
                "name": "Test HR Employee 2",
                "employee_number": "EMP-9999",
            }
        )
        self.assertEqual(employee.employee_number, "EMP-9999")

    def test_partner_with_existing_ids(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Partner With IDs",
                "is_customer": True,
                "is_vendor": True,
                "is_employee": True,
                "customer_number": "CUST-9999",
                "vendor_number": "VEND-9999",
                "employee_number": "EMP-9999",
            }
        )
        self.assertEqual(partner.customer_number, "CUST-9999")
        self.assertEqual(partner.vendor_number, "VEND-9999")
        self.assertEqual(partner.employee_number, "EMP-9999")

        # Test write with existing IDs doesn't overwrite
        partner.write(
            {
                "is_customer": True,
                "is_vendor": True,
                "is_employee": True,
            }
        )
        self.assertEqual(partner.customer_number, "CUST-9999")
        self.assertEqual(partner.vendor_number, "VEND-9999")
        self.assertEqual(partner.employee_number, "EMP-9999")

    def test_write_remove_boolean(self):
        partner = self.env["res.partner"].create({"name": "Test Write Partner False"})
        partner.write(
            {
                "is_customer": False,
                "is_vendor": False,
                "is_employee": False,
            }
        )
        self.assertFalse(partner.customer_number)
        self.assertFalse(partner.vendor_number)
        self.assertFalse(partner.employee_number)
