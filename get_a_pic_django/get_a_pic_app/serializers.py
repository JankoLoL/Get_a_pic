from rest_framework import serializers
from .models import UserProfile, Image, Plan, ThumbnailSize, ExpiringLink
from PIL import Image as PILImage


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

    image_file = serializers.ImageField(help_text="Only JPG or PNG format allowed")

    class Meta:
        model = Image
        fields = ('id', 'user', 'image_file', 'uploaded_at', 'thumbnail_200', 'thumbnail_400')

    def validate_image_file(self, value):
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in ['jpg', 'png']:
            raise serializers.ValidationError("Invalid image format! Only JPG or PNG allowed")
        try:
            image = PILImage.open(value)
            image.verify()
        except Exception:
            raise serializers.ValidationError("Invalid or corrupted image")

        return value


def _get_thumbnail_url(self, obj, size):
    file_extension = obj.image_file.name.split(".")[-1].lower()
    return f"/media/thumbnails/{obj.id}_{size}.{file_extension}"


def get_thumbnail_200(self, obj):
    return self._get_thumbnail_url(obj, 200) if self.should_include_thumbnail(obj, 200) else None


def get_thumbnail_400(self, obj):
    return self._get_thumbnail_url(obj, 400) if self.should_include_thumbnail(obj, 400) else None


def should_include_thumbnail(self, obj, size):
    user_plan = obj.user.profile.plan.name
    if size == 200:
        return user_plan in ['Basic', 'Premium', 'Enterprise']
    elif size == 400:
        return user_plan in ['Premium', 'Enterprise']
    return False


def should_include_original_link(self, obj):
    user_plan = obj.user.profile.plan.name
    return user_plan in ['Premium', 'Enterprise']


def to_representation(self, instance):
    rep = super().to_representation(instance)

    if not self.should_include_original_link(instance):
        rep.pop('image_file', None)

    return {key: value for key, value in rep.items() if value is not None}


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    plan = PlanSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'plan', 'images')


class ExpiringLinkSerializer(serializers.ModelSerializer):
    expiration_seconds = serializers.IntegerField(
        write_only=True,
        required=True,
        min_value=300,
        max_value=30000,
        help_text="Set expiration time in seconds (between 300 and 30000)"
    )
    expiration_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ExpiringLink
        fields = ['image', 'link', 'expiration_date', 'expiration_seconds']
