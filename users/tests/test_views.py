from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from carts.models import Cart


class UserViewsTestCase(TestCase):
    def setUp(self):
        # Set up a test client and user for use in all test methods
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123", phone_number="1234567890"
        )
        self.login_url = reverse("user:login")
        self.registration_url = reverse("user:registration")
        self.profile_url = reverse("user:profile")
        self.logout_url = reverse("user:logout")

    def test_login_view(self):
        # Test the login view with valid credentials
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpassword123"}
        )
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(self.user.is_authenticated)

    def test_registration_view(self):
        # Test the registration view with valid form data
        response = self.client.post(
            self.registration_url,
            {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "john@example.com",
                "password1": "12345678!!",
                "password2": "12345678!!",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect status code
        new_user = User.objects.get(username="johndoe")
        self.assertTrue(new_user.is_authenticated)

    def test_profile_view_authenticated(self):
        # Test the profile view when the user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)  # Success status code
        self.assertTemplateUsed(response, "users/profile.html")

    def test_profile_view_unauthenticated(self):
        # Test the profile view redirects when the user is not authenticated
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_logout_view(self):
        # Test the logout view
        self.client.force_login(self.user)
        self.client.logout()
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertFalse(self.user.is_authenticated)

    def test_logout_view(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, reverse("main:index"))
        self.client.logout()
        self.assertNotIn("_auth_user_id", self.client.session)
