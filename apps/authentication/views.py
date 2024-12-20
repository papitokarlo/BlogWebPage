from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegisterSerializer,
    ActivateSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    CustomUserSerializer
)
from .models import CustomUser


class RegisterViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'activate':
            return ActivateSerializer
        else:
            return RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            activation_link = request.build_absolute_uri(
                reverse("register-activate", kwargs={"uidb64": uid, "token": token})
            )
            send_mail(
                "Activate Your Account",
                f"Click the link to activate your account: {activation_link}",
                "begadze.zura@gmail.com",
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "User registered. Activation email sent."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="activate/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)")
    def activate(self, request, uidb64, token):
        serializer = self.get_serializer_class()(data={'uidb64': uidb64, 'token': token})
        if serializer.is_valid():
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Account activated successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.GenericViewSet):
    permission_classes = []
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                if not user.is_active:
                    return Response(
                        {"error": "Account is not activated. Please check your email."},
                        status=status.HTTP_403_FORBIDDEN,
                    )
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "username": user.username,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetViewSet(viewsets.GenericViewSet):
    permission_classes = []
    serializer_class = PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset link sent to email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmViewSet(viewsets.GenericViewSet):
    permission_classes = []
    serializer_class = PasswordResetConfirmSerializer

    @action(detail=False, methods=["post"], url_path="password-reset-confirm/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)")
    def password_reset_confirm(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(uidb64, token)
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def update(self, request, *args, **kwargs):
        user = request.user
        requested_user = self.get_object()
        if user != requested_user:
            return Response({"error": "User doesn't match"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        if user:
            serialized_user = self.serializer_class(user, context={'request': request})
            return Response(serialized_user.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Something went wrong during logout."},
                status=status.HTTP_400_BAD_REQUEST,
            )

