from django.test import TestCase
from goods.models import Categories, Products
from decimal import Decimal


class CategoriesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Categories.objects.create(
            id=1, name="Electronics", slug="electronics", sort=1, is_visible=True
        )

    def test_name_label(self):
        category = Categories.objects.get(id=1)
        field_label = category._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_slug_label(self):
        category = Categories.objects.get(id=1)
        field_label = category._meta.get_field("slug").verbose_name
        self.assertEqual(field_label, "slug")

    def test_is_visible_default(self):
        category = Categories.objects.get(id=1)
        self.assertTrue(category.is_visible)

    def test_ordering(self):
        self.assertEqual(Categories._meta.ordering, ["sort"])

    def test_object_name_is_name(self):
        category = Categories.objects.get(id=1)
        expected_object_name = category.name
        self.assertEqual(expected_object_name, str(category))

    def test_user_meta_options(self):
        self.assertEqual(Categories._meta.db_table, "category")
        self.assertEqual(Categories._meta.verbose_name, "Category")
        self.assertEqual(Categories._meta.verbose_name_plural, "Categories")


class ProductsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(
            name="Electronics", slug="electronics", sort=1
        )
        Products.objects.create(
            id=1,
            name="Laptop",
            slug="laptop",
            description="Portable computer",
            price=Decimal("999.99"),
            discount=Decimal("10.00"),
            quantity=5,
            category=category,
            is_visible=True,
        )

    def test_name_label(self):
        product = Products.objects.get(id=1)
        field_label = product._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_get_absolute_url(self):
        product = Products.objects.get(id=1)
        self.assertEqual(product.get_absolute_url(), "/catalog/product/laptop/")

    def test_total_price(self):
        product = Products.objects.get(id=1)
        expected_price = Decimal("899.99")  # 999.99 - 10% discount
        self.assertEqual(product.total_price(), expected_price)

    def test_display_id(self):
        product = Products.objects.get(id=1)
        expected_display_id = "id: 00001"
        self.assertEqual(product.display_id(), expected_display_id)

    def test_str_method(self):
        product = Products.objects.get(id=1)
        expected_object_name = "Laptop"
        self.assertEqual(str(product), expected_object_name)
