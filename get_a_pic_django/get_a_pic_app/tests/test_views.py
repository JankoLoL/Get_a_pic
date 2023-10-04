from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import UserProfile, Image, Plan, ThumbnailSize, User


class MainPageViewTest(TestCase):
    def test_main_page_response(self):
        client = APIClient()
        response = client.get(reverse('main-page'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), "Welcome on main page")


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
        self.plan = Plan.objects.create(name="Basic")

    def test_get_plans(self):
        response = self.client.get(reverse('plan-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ThumbnailSizeViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.thumbnail_size = ThumbnailSize.objects.create(size=200)

    def test_get_thumbnail_sizes(self):
        response = self.client.get(reverse('thumbnailsize-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


