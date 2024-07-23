from django.test import TestCase
from django.urls import reverse  # Used to generate URLs

from main.views import index, about  # Assuming your views are in the same directory as tests


class HomeTest(TestCase):

    def test_index_view(self):
        """Test the index view returns a successful response with the correct context."""
        response = self.client.get(reverse('main:index'))  # Use reverse to generate URL
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home place")  # Check for title in response
        self.assertContains(response, "Furniture store HOME PLACE")  # Check for content

    def test_about_view(self):
        """Test the about view returns a successful response with the correct context."""
        response = self.client.get(reverse('main:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About us")  # Check for title in response
        self.assertContains(response, "HOME PLACE is the best furniture store in the world")  # Check for content on page
    
    
    class ContactViewTestCase(TestCase):
        def test_contact_view(self):
            """Test the contact view returns a successful response with the correct context."""
            response = self.client.get(reverse('main:contact'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Contact Us")  # Check for title in response
            self.assertContains(response, "Send Message")  # Check for content on page

        def test_valid_contact_form_submission(self):
            """Test submitting a valid contact form."""
            form_data = {
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '+380123456789',
                'comment': 'Hello, this is a test message.',
            }
            response = self.client.post(reverse('main:contact'), form_data)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Thank you for your question, we will contact you as soon as possible.")

        def test_invalid_contact_form_submission(self):
            """Test submitting an invalid contact form."""
            form_data = {
                'name': '',  # Missing name
                'email': 'invalid-email',  # Invalid email format
                'phone': '12345',  # Invalid phone format
                'comment': 'Hello, this is a test message.',
            }
            response = self.client.post(reverse('main:contact'), form_data)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "There were errors in your form. Please correct and try again.")