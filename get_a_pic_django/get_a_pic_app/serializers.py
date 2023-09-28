from rest_framework import serializers
from .models import UserProfile, Image, Plan, ThumbnailSize


class ThumbnailSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailSize
        fields = ('id', 'size')


class PlanSerializer(serializers.ModelSerializer):
    thumbnail_size = ThumbnailSizeSerializer(many=True)

    class Meta:
        model = Plan
        fields = ('id', 'name', 'thumbnail_size', 'has_original_image_link', 'can_generate_expiring_link')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'user', 'image_file', 'uploaded_at')


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    plan = PlanSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'plan')
