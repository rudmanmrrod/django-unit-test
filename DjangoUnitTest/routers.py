from rest_framework.routers import DefaultRouter
from users.viewset import ProfileViewSet

router = DefaultRouter()

router.register(r'profile', ProfileViewSet)