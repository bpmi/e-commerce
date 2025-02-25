# Copyright 2019 Tecnativa - Sergio Teruel
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("-at_install", "post_install")
class WebsiteSaleHttpCase(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Remove this variable in v16 and put instead:
        # from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
        DISABLED_MAIL_CONTEXT = {
            "tracking_disable": True,
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        # Models
        ProductAttribute = cls.env["product.attribute"]
        ProductAttributeValue = cls.env["product.attribute.value"]
        ProductAttributeLine = cls.env["product.template.attribute.line"]
        cls.product_attribute = ProductAttribute.create(
            {"name": "Test Special Color", "create_variant": "no_variant"}
        )
        cls.product_attribute_value_red = ProductAttributeValue.create(
            {"name": "Test red", "attribute_id": cls.product_attribute.id}
        )
        cls.product_attribute_value_green = ProductAttributeValue.create(
            {"name": "Test green", "attribute_id": cls.product_attribute.id}
        )
        cls.product_attribute_value_blue = ProductAttributeValue.create(
            {"name": "Test blue", "attribute_id": cls.product_attribute.id}
        )
        cls.product_template = cls.env.ref("product.product_product_4_product_template")
        cls.product_attribute_line = ProductAttributeLine.create(
            {
                "product_tmpl_id": cls.product_template.id,
                "attribute_id": cls.product_attribute.id,
                "value_ids": [
                    (
                        6,
                        0,
                        [
                            cls.product_attribute_value_red.id,
                            cls.product_attribute_value_green.id,
                        ],
                    )
                ],
            }
        )
        cls.product_template.write(
            {"attribute_line_ids": [(4, cls.product_attribute_line.id)]}
        )
        cls.product_template_27 = cls.env.ref(
            "product.product_product_27_product_template"
        )
        cls.product_attribute_line_27 = ProductAttributeLine.create(
            {
                "product_tmpl_id": cls.product_template_27.id,
                "attribute_id": cls.product_attribute.id,
                "value_ids": [
                    (
                        6,
                        0,
                        [
                            cls.product_attribute_value_red.id,
                            cls.product_attribute_value_blue.id,
                        ],
                    )
                ],
            }
        )
        cls.product_template_27.write(
            {"attribute_line_ids": [(4, cls.product_attribute_line_27.id)]}
        )
        # Active attribute's filter in /shop. By default it's disabled.
        cls.env.ref("website_sale.products_attributes").active = True

    def test_ui_website(self):
        """Test frontend tour."""
        tour = (
            "odoo.__DEBUG__.services['web_tour.tour']",
            "website_sale_product_attribute_value_filter_existing",
        )
        self.browser_js(
            url_path="/",
            code="%s.run('%s')" % tour,
            ready="%s.tours['%s'].ready" % tour,
            login="admin",
        )
