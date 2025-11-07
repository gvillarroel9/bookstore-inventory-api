from django.urls import path, include
from rest_framework import routers
from inventory.views import BookViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('api/', include(router.urls)),
]