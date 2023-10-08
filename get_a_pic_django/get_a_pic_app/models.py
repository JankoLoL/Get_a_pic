import secrets
from django.utils import timezone

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


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to="uploaded_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def create_thumbnail(self, size):
        try:
            img = PilImage.open(self.image_file)

            aspect = img.width / img.height
            new_width = int(size * aspect)

            img = img.resize((new_width, size))

            file_extension = self.image_file.name.split('.')[-1].lower()

            thumb_path = f"thumbnails/{self.id}_{size}.{file_extension}"
            file_format = file_extension.upper()
            if file_format == "JPG":
                file_format = "JPEG"

            img.save(f"{settings.MEDIA_ROOT}/{thumb_path}", file_format)

            thumbnail_size = ThumbnailSize.objects.get(size=size)
            Thumbnail.objects.create(image=self, thumbnail_size=thumbnail_size, file_path=thumb_path)

            return thumb_path

        except Exception as e:
            raise ValueError(f"Error creating thumbnail for image {self.id}: {str(e)}")

    def __str__(self):
        return f"Image {self.id} by {self.user.username}"


class Thumbnail(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='thumbnails')
    thumbnail_size = models.ForeignKey(ThumbnailSize, on_delete=models.CASCADE, related_name='thumbnails')
    file_path = models.CharField(max_length=500)

    def __str__(self):
        return f"Thumbnail {self.id} of size {self.thumbnail_size} for Image {self.image.id}"


class ExpiringLink(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    link = models.CharField(max_length=50, default=secrets.token_urlsafe, unique=True)

    expiration_date = models.DateTimeField(null=True)

    def is_expired(self):
        return self.expiration_date < timezone.now()
