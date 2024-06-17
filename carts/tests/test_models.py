from django.test import TestCase
from users.models import User
from goods.models import Categories
from goods.models import Products
from carts.models import Cart

from decimal import Decimal


class CartModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Created a user
        cls.user = User.objects.create(username="testuser", password="12345")
        # Created a category
        cls.category = Categories.objects.create(
            name="Electronics", slug="electronics", sort=1
        )
        # Created a product
        cls.product = Products.objects.create(
            name="Laptop",
            slug="laptop",
            description="Portable computer",
            price=Decimal("100.00"),
            quantity=2,
            category=cls.category,
        )

        # Created a cart
        cls.cart = Cart.objects.create(user=cls.user, product=cls.product, quantity=2)

    def test_product_price(self):
        # Checking the correctness of the product price calculation
        self.assertEqual(self.cart.product_price(), 200.00)

    def test_total_cart_price(self):
        # Checking the sum of prices for all products in the basket
        total_price = Cart.objects.total_cart_price()
        self.assertEqual(total_price, 200.00)

    def test_total_cart_quantity(self):
        # Checking the total number of products in the baske
        total_quantity = Cart.objects.total_cart_quantity()
        self.assertEqual(total_quantity, 2)

    def test_str_method(self):
        # Checking the __str__ method
        cart_str = str(self.cart)
        self.assertEqual(cart_str, "Cart testuser | Product Laptop | Quantity 2 ")

    def test_cart_creation(self):
        # Checking the creation of the shopping cart
        self.assertIsInstance(self.cart, Cart)
        self.assertEqual(self.cart.user.username, "testuser")
        self.assertEqual(self.cart.product.name, "Laptop")
        self.assertEqual(self.cart.quantity, 2)
