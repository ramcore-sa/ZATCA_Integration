"""A Company customer with no Country gets the system's own (no site/DB).

ERPNext's setup wizard demo data creates Company customers without this app's
Country field, and the refusal in ``overrides.customer.validate`` failed the
whole demo. ``default_customer_country`` takes the system country as a
function, so a dict stands in for the document and nothing touches a database.
"""

import unittest


class _Doc(dict):
    def set(self, key, value):
        self[key] = value


class TestDefaultCustomerCountry(unittest.TestCase):
    def setUp(self):
        from zatca_integration.overrides.customer import default_customer_country

        self.fill = default_customer_country

    def test_an_empty_company_customer_gets_the_system_country(self):
        doc = _Doc(customer_type="Company", custom_country="")
        self.fill(doc, get_default=lambda: "Saudi Arabia")
        self.assertEqual(doc["custom_country"], "Saudi Arabia")

    def test_an_entered_country_is_never_touched(self):
        doc = _Doc(customer_type="Company", custom_country="United Arab Emirates")
        self.fill(doc, get_default=lambda: "Saudi Arabia")
        self.assertEqual(doc["custom_country"], "United Arab Emirates")

    def test_individuals_are_left_alone(self):
        doc = _Doc(customer_type="Individual", custom_country="")
        self.fill(doc, get_default=lambda: "Saudi Arabia")
        self.assertEqual(doc["custom_country"], "")

    def test_with_no_system_country_the_field_stays_empty(self):
        doc = _Doc(customer_type="Company", custom_country=None)
        self.fill(doc, get_default=lambda: None)
        self.assertIsNone(doc["custom_country"])


if __name__ == "__main__":
    unittest.main()
