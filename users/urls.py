from django.urls import path
from users.apps import UsersConfig
from users.views import (
    PaymentListAPIView,
    CustomUserCreateAPIView,
    CustomUserListAPIView,
    CustomUserRetrieveAPIView,
    CustomUserUpdateAPIView,
    CustomUserDestroyAPIView,
    PaymentCreateAPIView,
    PaymentRetrieveAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name


urlpatterns = [
    # payment_routes
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment_detail"),
    # customuser_routes
    path("user/", CustomUserListAPIView.as_view(), name="user_list"),
    path("user/create/", CustomUserCreateAPIView.as_view(), name="user_create"),
    path("user/<int:pk>/", CustomUserRetrieveAPIView.as_view(), name="user_detail"),
    path("user/update/<int:pk>/", CustomUserUpdateAPIView.as_view(), name="user_update"),
    path("user/delete/<int:pk>/", CustomUserDestroyAPIView.as_view(), name="user_delete"),
    # token_routes
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
