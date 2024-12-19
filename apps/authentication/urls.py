from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.authentication.views import (
    RegisterViewSet,
    LoginViewSet,
    PasswordResetViewSet,
    PasswordResetConfirmViewSet,
    UserViewSet,
)

router = DefaultRouter()


router.register('register', RegisterViewSet, basename='register')
router.register('login', LoginViewSet, basename='login')
router.register('password-reset', PasswordResetViewSet, basename='password-reset')
router.register('', PasswordResetConfirmViewSet, basename='password-reset-confirm')
router.register('user', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]