from rest_framework import serializers
from .models import UserProfile, Image, Plan, ThumbnailSize


class ThumbnailSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailSize
        fields = ('id', 'size')


class PlanSerializer(serializers.ModelSerializer):
    thumbnail_sizes = ThumbnailSizeSerializer(many=True)

    class Meta:
        model = Plan
        fields = ('id', 'name', 'thumbnail_sizes', 'has_original_image_link', 'can_generate_expiring_link')


class ImageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    thumbnail_200 = serializers.SerializerMethodField()
    thumbnail_400 = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'user', 'image_file', 'uploaded_at', 'thumbnail_200', 'thumbnail_400')

    def _get_thumbnail_url(self, obj, size):
        file_extension = obj.image_file.name.split(".")[-1].lower()
        return f"/media/thumbnails/{obj.id}_{size}.{file_extension}"

    def get_thumbnail_200(self, obj):
        return self._get_thumbnail_url(obj, 200)

    def get_thumbnail_400(self, obj):
        return self._get_thumbnail_url(obj, 400)


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    plan = PlanSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'plan', 'images')
