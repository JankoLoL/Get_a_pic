import os

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import UserProfile, Image, Plan, ThumbnailSize, User
from django.core.files.uploadedfile import SimpleUploadedFile


class MainPageViewTest(TestCase):
    def test_main_page_response(self):
        client = APIClient()
        response = client.get(reverse('main-page'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), "<h1>Welcome on main page!</h1>")


class UserProfileViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_get_own_profile(self):
        response = self.client.get(reverse('userprofile-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_cannot_access_other_profiles(self):
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        response = self.client.get(reverse('userprofile-list'))
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['user'], another_user.id)


class PlanViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='adminuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.plan = Plan.objects.create(name="Basic")

    def test_get_plans(self):
        response = self.client.get(reverse('plan-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ThumbnailSizeViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.thumbnail_size = ThumbnailSize.objects.create(size=200)
        self.user = User.objects.create_superuser(username='adminuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.user.profile.save()

    def test_get_thumbnail_sizes(self):
        response = self.client.get(reverse('thumbnailsize-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ImageViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        some_plan = Plan.objects.create(name='Enterprise')
        self.user.profile.plan = some_plan
        self.user.profile.save()

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.current_dir, 'test_image.jpg')

        with open(self.image_path, 'rb') as img_file:
            self.image_file = SimpleUploadedFile(
                name='test_image.jpg',
                content=img_file.read(),
                content_type='image/jpeg'
            )
            self.wrong_file = SimpleUploadedFile(
                name='test.txt',
                content=b"Wrong type of content",
                content_type='text/plain'
            )

    def test_see_own_images(self):
        Image.objects.create(user=self.user, image_file=self.image_file)

        response = self.client.get(reverse('image-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_no_access_for_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('image-list'))
        self.assertEqual(response.status_code, 403)

    def test_upload_correct_image(self):
        response = self.client.post(reverse('image-list'), {'image_file': self.image_file}, format='multipart')
        self.assertEqual(response.status_code, 201)

    def test_upload_without_permission(self):
        self.client.logout()
        response = self.client.post(reverse('image-list'), {'image-file': self.image_file}, format='multipart')
        self.assertEqual(response.status_code, 403)

    def test_upload_wrong_type(self):
        response = self.client.post(reverse('image-list'), {'image-file': self.image_file}, format='multipart')
        self.assertEqual(response.status_code, 400)
