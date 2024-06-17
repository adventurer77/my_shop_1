from django.test import TestCase
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.contrib.auth import get_user_model

class UserFormsTest(TestCase):

    def test_false_user_login_form(self):
        """
        Test that the form validates with incorrect data for user login.
        """
        form_data = {'username': 'johndoe', 'password': '12345678!!'}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_user_registration_form(self):
        """
        Test that the form validates with correct data for user creation.
        """
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password1': '12345678!!',
            'password2': '12345678!!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        new_user = form.save()
        self.assertEqual(new_user.username, "johndoe")
        self.assertEqual(new_user.email, "john@example.com")

    def test_user_registration_form_password_mismatch(self):
        """
        Test that the form fails validation with an invalid password2.
        """
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password1': '12345678!!',
            'password2': '54321'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_user_registration_form_invalid_email(self):
        """
        Test that the form fails validation with an invalid email address.
        """
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'jinvalid',
            'password1': '12345678!!',
            'password2': '12345678!!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
    
    def test_user_registration_form_invalid_username(self):
        """
        Test that the form fails validation with an invalid username.
        """
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe!', # Username with special character
            'email': 'john@example.com',
            'password1': '12345678!!',
            'password2': '12345678!!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class ProfileFormTest(TestCase):

    def setUp(self):
        """
        Create a test user for profile update.
        """
        self.user = get_user_model().objects.create_user(username="test_user", email="testemail@example.com", password="testpassword")

    def test_valid_profile_update(self):
        """
        Test that the form validates with correct data for profile update.
        """
        data = {
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
            "username": "updated_username",
            "email": "updated_email@example.com",
        }
        form = ProfileForm(instance=self.user, data=data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated First Name")
        self.assertEqual(self.user.last_name, "Updated Last Name")
        self.assertEqual(self.user.username, "updated_username")
        self.assertEqual(self.user.email, "updated_email@example.com")

    def test_invalid_username(self):
        """
        Test that the form fails validation with an invalid username.
        """
        data = {
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
            "username": "invalid_username!",  # Username with special character
            "email": "updated_email@example.com",
        }
        form = ProfileForm(instance=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_invalid_email(self):
        """
        Test that the form fails validation with an invalid email address.
        """
        data = {
            "first_name": "Updated First Name",
            "last_name": "Updated Last Name",
            "username": "updated_username",
            "email": "invalidemail",  # Invalid email format
        }
        form = ProfileForm(instance=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)