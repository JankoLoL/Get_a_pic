from django.db import models
from django.contrib.auth.models import User


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


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to="uploaded_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} by {self.user.username}"
