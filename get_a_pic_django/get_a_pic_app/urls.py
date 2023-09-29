from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, ImageViewSet, MainPageView
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'userprofile', UserProfileViewSet)
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('', MainPageView.as_view(), name='main-page'),
    path('api/', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='admin/logout.html'), name='logout'),

]
