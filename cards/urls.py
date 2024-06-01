from rest_framework.routers import DefaultRouter
from django.urls import path, include
from cards import views


router = DefaultRouter()
router.register(r'cards', views.CardViewSet, basename='cards')

urlpatterns = [
    path('', include(router.urls))
]
