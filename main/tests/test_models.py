from django.test import TestCase
from main.models import Contact

class ContactModelTestCase(TestCase):
    def test_contact_model_str(self):
        """Test the __str__ method of the Contact model."""
        contact = Contact.objects.create(
            name='John Doe',
            email='john@example.com',
            phone='+380123456789',
            comment='Hello, this is a test message.',
        )
        expected_str = f'John Doe - Created: {contact.date_created} | Updated: {contact.date_updated}'
        self.assertEqual(str(contact), expected_str)

    def test_contact_model_ordering(self):
        """Test the ordering of Contact model by date_created."""
        contact1 = Contact.objects.create(name='Contact 1', email='contact1@example.com', phone='+380111111111')
        contact2 = Contact.objects.create(name='Contact 2', email='contact2@example.com', phone='+380222222222')
        contact3 = Contact.objects.create(name='Contact 3', email='contact3@example.com', phone='+380333333333')

        contacts = Contact.objects.all().order_by('-date_created')
        self.assertEqual(contacts[0], contact1)
        self.assertEqual(contacts[1], contact2)
        self.assertEqual(contacts[2], contact3)
    
    def test_contact_model_is_confirmed_default(self):
        """Test that is_confirmed field defaults to False."""
        contact = Contact.objects.create(name='John Doe', email='john@example.com', phone='+380123456789')
        self.assertFalse(contact.is_confirmed)