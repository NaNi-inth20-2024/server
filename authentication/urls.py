from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import RegisterView, CustomTokenObtainPairView, UserInfoView

urlpatterns = [
    path("token", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("register", RegisterView.as_view()),
    path("user", UserInfoView.as_view()),
]
