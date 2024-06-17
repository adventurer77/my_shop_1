from django.test import TestCase, Client
from django.urls import reverse
from goods.models import Categories, Products
from carts.models import Cart
from users.models import User


class CartViewTestCase(TestCase):
    def setUp(self):
        # Created a client
        self.client = Client()
        # Created a user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123", phone_number="1234567890"
        )
        # Created a category
        self.category = Categories.objects.create(
            name="Electronics", slug="electronics", sort=1
        )
        # Created a product
        self.product = Products.objects.create(
            name="Laptop",
            slug="laptop",
            description="Portable computer",
            price=("100.00"),
            quantity=2,
            category=self.category,
        )

        # Created a add cart url
        self.add_cart_url = reverse("cart:cart_add")

    def test_cart_add_authenticated(self):
        # Test adding a product to the cart when the user is authenticated
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(self.add_cart_url, {"product_id": self.product.id})
        cart = Cart.objects.filter(user=self.user, product=self.product).first()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(cart)
        self.assertEqual(cart.quantity, 1)

    def test_cart_add_unauthenticated(self):
        # Test adding a product to the cart when the user is not authenticated
        session = self.client.session
        session["session_key"] = "test_session_key"
        session.save()
        response = self.client.post(self.add_cart_url, {"product_id": self.product.id})

        cart, created = Cart.objects.get_or_create(
            session_key="test_session_key",
            product=self.product,
            defaults={"quantity": 1},
        )

        self.assertTrue(created, "Cart was not created.")
        self.assertEqual(cart.quantity, 1, "The quantity of the cart is not correct.")

        self.assertEqual(response.status_code, 200, "Response status code is not 200.")
        self.assertIsNotNone(cart, "Cart does not exist.")

    def test_cart_change(self):
        # Test changing the quantity of a product in the cart
        self.cart = Cart.objects.create(
            user=self.user, product=self.product, quantity=1
        )
        self.change_cart_url = reverse("cart:cart_change")

        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            self.change_cart_url, {"cart_id": self.cart.id, "quantity": 3}
        )
        self.cart.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.quantity, 3)
        self.assertIn("quantity", response.json())
        self.assertEqual(response.json()["quantity"], "3")

    def test_cart_remove(self):
        # Test removing a product from the cart
        self.cart = Cart.objects.create(
            user=self.user, product=self.product, quantity=1
        )
        self.remove_cart_url = reverse("cart:cart_remove")

        self.client.login(username="testuser", password="testpassword123")
        response = self.client.post(
            self.remove_cart_url,
            {"cart_id": self.cart.id},
            HTTP_REFERER="orders:create_order",
        )

        with self.assertRaises(Cart.DoesNotExist):
            self.cart.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Product removed from cart")
