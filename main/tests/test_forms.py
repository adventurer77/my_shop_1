from django.test import TestCase
from main.forms import ContactForm

class ContactFormTestCase(TestCase):
    def test_valid_contact_form(self):
        """Test submitting a valid contact form."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+380123456789',
            'comment': 'Hello, this is a test message.',
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_contact_form(self):
        """Test submitting an invalid contact form."""
        form_data = {
            'name': '',  # Missing name
            'email': 'invalid-email',  # Invalid email format
            'phone': '12345',  # Invalid phone format
            'comment': 'Hello, this is a test message.',
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('phone', form.errors)