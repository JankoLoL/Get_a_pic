from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..models import Image, UserProfile, Plan, ThumbnailSize
from django.contrib.auth.models import User
import os
from django.db import IntegrityError
from django.conf import settings


class ImageModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.current_dir, 'test_image.jpg')
        ThumbnailSize.objects.create(size=200)
        ThumbnailSize.objects.create(size=400)

        with open(self.image_path, 'rb') as file:
            image_content = file.read()

        uploaded_image = SimpleUploadedFile(name='test_image.jpg', content=image_content, content_type='image/jpeg')
        self.image = Image.objects.create(image_file=uploaded_image, user=self.user)

    def test_image_creation(self):
        self.assertIsInstance(self.image, Image)
        self.assertIn('test_image', self.image.image_file.name)

    def test_image_string_representation(self):
        self.assertEqual(str(self.image), f"Image {self.image.id} by {self.user.username}")

    def test_create_thumbnails(self):
        sizes = [200, 400]
        for size in sizes:
            thumbnail_path = self.image.create_thumbnail(size=size)
            expected_path_format = f"thumbnails/{self.image.id}_{size}.jpg"
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

    def test_user_profile_created_on_user_creation(self):
        self.assertIsNotNone(self.user.profile)

    def test_user_is_authenticated(self):
        self.assertTrue(self.user.is_authenticated)

    def test_username_uniqueness(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="testuser", password="testpassword2")

    def test_one_to_one_relationship(self):
        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(user=self.user)


class UserProfileModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.profile = self.user.profile
        self.size_200 = ThumbnailSize.objects.create(size=200)
        self.size_400 = ThumbnailSize.objects.create(size=400)

        self.basic_plan = Plan.objects.create(name="Basic")
        self.basic_plan.thumbnail_sizes.add(self.size_200)

        self.premium_plan = Plan.objects.create(name="Premium", has_original_image_link=True)
        self.premium_plan.thumbnail_sizes.add(self.size_200, self.size_400)

        self.enterprise_plan = Plan.objects.create(name="Enterprise", has_original_image_link=True,
                                                   can_generate_expiring_link=True)
        self.enterprise_plan.thumbnail_sizes.add(self.size_200, self.size_400)

    def test_basic_plan_assigment(self):
        profile = self.user.profile
        profile.plan = self.basic_plan
        profile.save()
        self.assertEqual(profile.plan, self.basic_plan)
        self.assertIn(self.size_200, profile.plan.thumbnail_sizes.all())
        self.assertFalse(profile.plan.has_original_image_link)
        self.assertFalse(profile.plan.can_generate_expiring_link)

    def test_premium_plan_assignment(self):
        profile = self.user.profile
        profile.plan = self.premium_plan
        profile.save()
        self.assertEqual(profile.plan, self.premium_plan)
        self.assertIn(self.size_200, profile.plan.thumbnail_sizes.all())
        self.assertIn(self.size_400, profile.plan.thumbnail_sizes.all())
        self.assertTrue(profile.plan.has_original_image_link)
        self.assertFalse(profile.plan.can_generate_expiring_link)

    def test_enterprise_plan_assigment(self):
        profile = self.user.profile
        profile.plan = self.enterprise_plan
        profile.save()
        self.assertEqual(profile.plan, self.enterprise_plan)
        self.assertIn(self.size_200, profile.plan.thumbnail_sizes.all())
        self.assertIn(self.size_400, profile.plan.thumbnail_sizes.all())
        self.assertTrue(profile.plan.has_original_image_link)
        self.assertTrue(profile.plan.can_generate_expiring_link)


class UserProfileSignalTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password='testpassword')
        self.plan = Plan.objects.create(name="Basic")

    def test_create_user_creates_userprofile(self):
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_update_user_does_not_create_new_userprofile(self):
        self.assertEqual(UserProfile.objects.filter(user=self.user).count(), 1)

        self.user.username = "testuserchanged"
        self.user.save()

        self.assertEqual(UserProfile.objects.filter(user=self.user).count(), 1)


class PlanModelTestCase(TestCase):
    def setUp(self):
        self.thumbnail_size_200 = ThumbnailSize.objects.create(size=200)
        self.thumbnail_size_400 = ThumbnailSize.objects.create(size=400)
        self.plan = Plan.objects.create(name="Enterprise", has_original_image_link=True,
                                        can_generate_expiring_link=True)

    def test_plan_creation_with_name(self):
        self.assertEqual(self.plan.name, "Enterprise")

    def test_thumbnail_size_assignment(self):
        self.plan.thumbnail_sizes.add(self.thumbnail_size_200, self.thumbnail_size_400)
        self.assertIn(self.thumbnail_size_200, self.plan.thumbnail_sizes.all())
        self.assertIn(self.thumbnail_size_400, self.plan.thumbnail_sizes.all())

    def test_basic_plan_default_flags(self):
        basic_plan = Plan.objects.create(name="Basic")
        self.assertFalse(basic_plan.has_original_image_link)
        self.assertFalse(basic_plan.can_generate_expiring_link)

    def test_premium_plan_default_flags(self):
        premium_plan = Plan.objects.create(name="Premium", has_original_image_link=True)
        self.assertTrue(premium_plan.has_original_image_link)
        self.assertFalse(premium_plan.can_generate_expiring_link)

    def test_enterprise_plan_default_flags(self):
        self.assertTrue(self.plan.has_original_image_link)
        self.assertTrue(self.plan.can_generate_expiring_link)

    def test_basic_plan_modifications(self):
        basic_plan = Plan.objects.create(name="Basic")
        basic_plan.has_original_image_link = True
        basic_plan.can_generate_expiring_link = True
        basic_plan.save()

        self.assertTrue(basic_plan.has_original_image_link)
        self.assertTrue(basic_plan.can_generate_expiring_link)
