from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..models import Image
from django.contrib.auth.models import User
import os
from django.db import IntegrityError
from django.conf import settings


class ImageModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.current_dir, 'test_image.jpg')

        with open(self.image_path, 'rb') as file:
            image_content = file.read()

        uploaded_image = SimpleUploadedFile(name='test_image.jpg', content=image_content, content_type='image/jpeg')
        self.image = Image.objects.create(image_file=uploaded_image, user=self.user)

    def test_image_creation(self):
        self.assertIsInstance(self.image, Image)
        self.assertIn('test_image', self.image.image_file.name)

    def test_image_string_representation(self):
        self.assertEqual(str(self.image), f"Image {self.image.id} by {self.user.username}")

    def test_create_thumbnail(self):
        thumbnail_path = self.image.create_thumbnail(size=200)
        expected_path_format = f"thumbnails/{self.image.id}_200.jpg"
        self.assertEqual(thumbnail_path, expected_path_format)
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, thumbnail_path)))

    def test_image_belongs_to_user(self):
        self.assertEqual(self.image.user, self.user)


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
