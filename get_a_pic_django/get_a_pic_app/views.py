import io
import os.path
import secrets
from datetime import timedelta

from django.urls import reverse
from rest_framework import viewsets, views, status, serializers
from .models import UserProfile, Image, Plan, ThumbnailSize, ExpiringLink
from .serializers import UserProfileSerializer, ImageSerializer, PlanSerializer, \
    ThumbnailSizeSerializer, ExpiringLinkSerializer
from django.http import HttpResponse, FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.utils import timezone
from django.shortcuts import get_object_or_404


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.none()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.none()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)

            user_plan = self.request.user.profile.plan
            for thumbnail_size in user_plan.thumbnail_sizes.all():
                serializer.instance.create_thumbnail(thumbnail_size.size)

        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def create(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=request.data)

        if file_serializer.is_valid():
            try:
                self.perform_create(file_serializer)
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAdminUser]


class ThumbnailSizeViewSet(viewsets.ModelViewSet):
    queryset = ThumbnailSize.objects.all()
    serializer_class = ThumbnailSizeSerializer
    permission_classes = [IsAdminUser]


class MainPageView(views.APIView):

    def get(self, request):
        return HttpResponse("Welcome on main page")


class ExpiringLinkViewSet(viewsets.ModelViewSet):
    queryset = ExpiringLink.objects.all()
    serializer_class = ExpiringLinkSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):


        if request.user.profile.plan.name != 'Enterprise':
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        expiration_seconds = serializer.validated_data['expiration_seconds']

        image_id = serializer.validated_data.get('image').id

        try:
            image_instance = Image.objects.get(pk=image_id)
        except Image.DoesNotExist:
            return Response({"detail": "Image with provided ID does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        token = secrets.token_urlsafe(25)
        base_url = request._request.build_absolute_uri(reverse('retrieve_expiring_link', args=[token]))

        new_link = ExpiringLink(
            image=image_instance,
            link=token,
            expiration_date=timezone.now() + timedelta(seconds=expiration_seconds)
        )
        new_link.save()

        return Response({"link": base_url}, status=status.HTTP_201_CREATED)


class ExpiringLinkRetrieveView(APIView):
    def get(self, request, token):
        expiring_link = get_object_or_404(ExpiringLink, link=token)

        if expiring_link.is_expired():
            return Response({"detail": "Link has expired"}, status=status.HTTP_404_NOT_FOUND)

        image_path = expiring_link.image.image_file.path
        _, extension = os.path.splitext(image_path)

        if extension.lower() == '.jpeg' or extension.lower() == '.jpg':
            content_type = 'image/jpeg'
        elif extension.lower() == '.png':
            content_type = 'image/png'
        else:
            return Response({"detail": "Unsupported image format"}, status=status.HTTP_400_BAD_REQUEST)

        with open(image_path, 'rb') as file:
            content = file.read()

        return FileResponse(io.BytesIO(content), content_type=content_type)
