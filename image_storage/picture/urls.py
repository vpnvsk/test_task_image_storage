from django.urls import path, include
from rest_framework import routers

from . import views
from .views import ImageUploadAndListByUserViewSet

router = routers.DefaultRouter()
router.register(r'img', ImageUploadAndListByUserViewSet, basename='image')
urlpatterns = [
    path('img/<int:pk>/', views.ExpiringLinkCreateView.as_view(), name='create-expiring-link'),
    path('expiration/<str:link>/', views.ExpiringLinkView.as_view()),
    path('', include(router.urls)),
]