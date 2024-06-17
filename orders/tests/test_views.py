# 

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from carts.models import Cart
from goods.models import Categories, Products
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem

class OrderViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='John',
            password='testpassword123',
            phone_number='0956723419'
        )
        
        self.client.login(username='John', password='testpassword123')
        # Created a category
        self.category = Categories.objects.create(name='Electronics', slug='electronics', sort=1)
        # Created a product
        self.product = Products.objects.create(
            name='Laptop',
            slug='laptop',
            description='Portable computer',
            price=('100.00'),
            quantity=2,
            category=self.category
        )
        self.cart = Cart.objects.create(user=self.user, product=self.product, quantity=1)

    def test_create_order_view_post_valid(self):
        response = self.client.post(reverse('orders:create_order'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '0956723419',
            'requires_delivery': '1',
            'delivery_address': '123 Main St',
            'payment_on_get': '0',
        })
        self.assertRedirects(response, reverse('user:profile'), status_code=302)
        order = Order.objects.first()
        order_item = OrderItem.objects.first()
        
        # Check if the order fields are correctly filled
        self.assertEqual(order.user.username, 'John')
        self.assertEqual(order.phone_number, '0956723419')
        
        # Check if the order item fields are correctly filled
        self.assertEqual(order_item.product.name, 'Laptop')
        self.assertEqual(order_item.quantity, 1)
        
    def test_create_order_view_post_invalid_form(self):
        response = self.client.post(reverse('orders:create_order'), {
            'first_name': 'John',
            'last_name': 'Doe',
            # Missing phone_number and other required fields
        })
        
        self.assertEqual(response.status_code, 200)  # No redirect due to form errors
        self.assertFalse(Order.objects.exists())
        
        # Check if form errors are returned in the response context
        form_errors = response.context['form'].errors
        self.assertIn('phone_number', form_errors)

    def test_create_order_view_post_insufficient_quantity(self):
        # Set product quantity to 0 to simulate insufficient stock
        self.product.quantity = 0
        self.product.save()

        response = self.client.post(reverse('orders:create_order'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '0956723419',
            'requires_delivery': '1',
            'delivery_address': '123 Main St',
            'payment_on_get': '0',
        })
        
        # Check if the product quantity remains unchanged after an attempted order creation
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 0)
        
        # Check if the user's cart remains unchanged after an attempted order creation
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.quantity, 1)
        
    def test_create_order_view_get_request(self):
        response = self.client.get(reverse('orders:create_order'))
        
        # Check if the form is initialized with user's first and last name
        form_initial_data = response.context['form'].initial
        self.assertEqual(form_initial_data['first_name'], self.user.first_name)
