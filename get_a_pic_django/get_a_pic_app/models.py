from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PilImage
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class ThumbnailSize(models.Model):
    size = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"{self.size}px"


class Plan(models.Model):
    name = models.CharField(max_length=255, unique=True)
    thumbnail_sizes = models.ManyToManyField(ThumbnailSize, blank=True)
    has_original_image_link = models.BooleanField(default=False)
    can_generate_expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to="uploaded_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def create_thumbnail(self, size):
        img = PilImage.open(self.image_file)

        aspect = img.width / img.height
        new_width = int(size * aspect)

        img = img.resize((new_width, size))

        file_extension = self.image_file.name.split('.')[-1].lower()

        if file_extension not in ['jpg', 'png']:
            raise ValueError("Invalid image format. Only JPG or PNG allowed")

        thumb_path = f"thumbnails/{self.id}_{size}.{file_extension}"
        img.save(f"{settings.MEDIA_ROOT}/{thumb_path}", file_extension.upper())
        return thumb_path

    def __str__(self):
        return f"Image {self.id} by {self.user.username}"
