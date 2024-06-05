from django.test import SimpleTestCase
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
        self.assertContains(response, "Adout us")  # Check for title in response
        self.assertContains(response, "HOME PLACE is the best furniture store in the world")  # Check for content on page