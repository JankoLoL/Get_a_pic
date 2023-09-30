from rest_framework import viewsets, views, status
from .models import UserProfile, Image, Plan, ThumbnailSize
from .serializers import UserProfileSerializer, ImageSerializer, PlanSerializer, ThumbnailSizeSerializer
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.none()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.none()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        image = Image.objects.get(pk=serializer.instance.id)

        user_plan = self.request.user.profile.plan
        for thumbnail_size in user_plan.thumbnail_sizes.all():
            image.create_thumbnail(thumbnail_size.size)

    def create(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=request.data)

        if file_serializer.is_valid():
            self.perform_create(file_serializer)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class ThumbnailSizeViewSet(viewsets.ModelViewSet):
    queryset = ThumbnailSize.objects.all()
    serializer_class = ThumbnailSizeSerializer


class MainPageView(views.APIView):

    def get(self, request):
        return HttpResponse("Welcome on main page")
