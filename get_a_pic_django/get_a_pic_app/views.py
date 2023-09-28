from rest_framework import viewsets, views
from .models import UserProfile, Image, Plan, ThumbnailSize
from .serializers import UserProfileSerializer, ImageSerializer, PlanSerializer, ThumbnailSizeSerializer
from django.http import HttpResponse


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class ThumbnailSizeViewSet(viewsets.ModelViewSet):
    queryset = ThumbnailSize.objects.all()
    serializer_class = ThumbnailSizeSerializer


class MainPageView(views.APIView):

    def get(self, request):
        return HttpResponse("Welcome on main page")
