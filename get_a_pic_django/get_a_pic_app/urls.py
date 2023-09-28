from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, ImageViewSet, MainPageView

router = DefaultRouter()
router.register(r'userprofile', UserProfileViewSet)
router.register(r'images', ImageViewSet)


urlpatterns = [
    path('', MainPageView.as_view(), name='main-page'),
    path('api/', include(router.urls))

]
