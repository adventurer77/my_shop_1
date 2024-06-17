from django.test import TestCase
from orders.models import Order, OrderItem
from goods.models import Categories,Products
from users.models import User


class OrderModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create(
            first_name='John', 
            last_name='Doe',
            username='johndoe',
            email='john@example.com',
            password='12345678!!',
            
        )

    def test_create_order(self):
        """
        Test that an Order object can be created with valid data.
        """
        order = Order.objects.create(
            user=self.user,
            phone_number="1234567890",
            requires_delivery=True,
            delivery_address="123 Main St",
            payment_on_get=True
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.phone_number, "1234567890")
        self.assertTrue(order.requires_delivery)
        self.assertEqual(order.delivery_address, "123 Main St")
        self.assertTrue(order.payment_on_get)
        self.assertFalse(order.is_paid)
        self.assertEqual(order.status, "In progress")

    def test_order_meta_options(self):
        self.assertEqual(Order._meta.db_table, 'order')
        self.assertEqual(Order._meta.verbose_name, 'Order')
        self.assertEqual(Order._meta.verbose_name_plural, 'Orders')

    def test_order_str_representation(self):
        """
        Test that the __str__ method returns the expected string representation.
        """
        order = Order.objects.create(user=self.user)
        self.assertEqual(str(order), f"Order № {order.pk} | Buyer {order.user.first_name} {order.user.last_name}")

    
class OrderItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Created a category
        category = Categories.objects.create(name='Electronics', slug='electronics', sort=1)
        # Created a product
        product = Products.objects.create(name='Laptop',
            slug='laptop',
            description='Portable computer',
            price=('100.00'),
            quantity=2,
            category=category)
        order = Order.objects.create(phone_number='1234567890')
        OrderItem.objects.create(order=order, product=product, name='Laptop', price=100.00, quantity=2)

    def test_order_item_creation(self):
        order_item = OrderItem.objects.get(id=1)
        self.assertEqual(order_item.name, 'Laptop')
        self.assertEqual(order_item.quantity, 2)

    def test_products_price(self):
        order_item = OrderItem.objects.get(id=1)
        self.assertEqual(order_item.products_price(), 200.00)

    def test_order_meta_options(self):
        self.assertEqual(OrderItem._meta.db_table, 'order_item')
        self.assertEqual(OrderItem._meta.verbose_name, 'Order_item')
        self.assertEqual(OrderItem._meta.verbose_name_plural, 'Order_items')
    

