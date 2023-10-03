from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..models import Image, User
import os
from django.db import IntegrityError


class ImageModelTestCase(TestCase):
    def test_image_creation(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'test_image.jpg')

        with open(image_path, 'rb') as file:
            image_content = file.read()

        uploaded_image = SimpleUploadedFile(name='test_image.jpg', content=image_content, content_type='image/jpeg')

        image = Image.objects.create(image_file=uploaded_image, user=user)

        self.assertIsInstance(image, Image)
        self.assertIn('test_image', image.image_file.name)


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_create_user_with_password(self):
        user = self.user
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))

    def test_user_is_authenticated(self):
        user = self.user
        self.assertTrue(user.is_authenticated)

    def test_username_uniqueness(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="testuser", password="testpassword2")
