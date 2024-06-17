from django.test import TestCase, Client
from django.urls import reverse
from goods.models import Products, Categories


class GoodsViewsTests(TestCase):

    def setUp(self):
        # Set up a test client, category, and product for use in all test methods
        self.client = Client()
        self.category = Categories.objects.create(
            name="Electronics", slug="electronics", sort=1
        )
        self.product = Products.objects.create(
            name="Laptop",
            slug="laptop",
            price=1000.00,
            discount=10,
            quantity=5,
            category=self.category,
        )

    def test_catalog_view(self):
        # Test to check the display of the catalog
        response = self.client.get(
            reverse("goods:index", kwargs={"category_slug": "electronics"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/catalog.html")
        self.assertIn("goods", response.context)

    def test_product_view(self):
        # Test to check the display of the product page.
        response = self.client.get(
            reverse("goods:product", kwargs={"product_slug": "laptop"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/product.html")
        self.assertIn("product", response.context)

    def test_catalog_view_all(self):
        # Test to check the display of the all catalog page
        response = self.client.get(
            reverse("goods:index", kwargs={"category_slug": "all"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "goods/catalog.html")
        self.assertIn("goods", response.context)

    # def test_catalog_view_no_category(self):
    #         response = self.client.get(reverse('goods:index', kwargs={'category_slug': 'non-existing'}))
    #         self.assertRedirects(response, reverse('main:index'))
