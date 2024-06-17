from django.test import TestCase
from orders.forms import CreateOrderForm

class CreateOrderFormTest(TestCase):

    def test_valid_data(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '0954692144',
            'requires_delivery': '1',
            'delivery_address': '123 Main St',
            'payment_on_get': '0',
        }
        form = CreateOrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number_letters(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': 'abcdefghijk',
            'requires_delivery': '1',
            'delivery_address': '123 Main St',
            'payment_on_get': '0',
        }
        form = CreateOrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_invalid_phone_number_format(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '+1234567',
            'requires_delivery': '1',
            'delivery_address': '123 Main St',
            'payment_on_get': '0',
        }
        form = CreateOrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_requires_delivery_field(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '0954692144',
            'requires_delivery': '1',
            'delivery_address': '123 Main St',
            'payment_on_get': '0',
        }
        form = CreateOrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['requires_delivery'], "1")

        form_data['requires_delivery'] = '0'  
        form = CreateOrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['requires_delivery'], "0")

    def test_optional_delivery_address(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '0954692144',
            'requires_delivery': '1',
            'delivery_address': '',
            'payment_on_get': '0',
        }
        form = CreateOrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_payment_on_get_field(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '0954692144',
            'requires_delivery': '1',
            'delivery_address': '123 Main St',
            'payment_on_get': '1',
        }
        form = CreateOrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['payment_on_get'], "1")

        form_data['payment_on_get'] = '0'  # False
        form = CreateOrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['payment_on_get'], "0")
