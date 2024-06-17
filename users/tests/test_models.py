from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User


class UserTestCase(TestCase):

    def setUp(self):
        """
        Creating a test user
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123", phone_number="1234567890"
        )
        # Adding an image for the user
        self.user.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=open("media/test/test_image.jpg", "rb").read(),
            content_type="image/jpeg",
        )
        self.user.save()

    def test_user_creation(self):
        """
        Checking if a user has been created
        """
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_user_phone_number(self):
        """
        Checking the correctness of saving the phone number
        """
        self.assertEqual(self.user.phone_number, "1234567890")

    def test_user_image_field(self):
        """
        Checking if an image has been added
        """
        self.assertIsNotNone(self.user.image)

    def test_user_str_method(self):
        """
        Checking  __str__ method
        """
        self.assertEqual(str(self.user), "testuser")

    def test_user_meta_options(self):
        """
        Validation of model metadata
        """
        self.assertEqual(self.user._meta.db_table, "User")
        self.assertEqual(self.user._meta.verbose_name, "User")
        self.assertEqual(self.user._meta.verbose_name_plural, "Users")
