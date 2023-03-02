from django.urls import include, path
from rest_framework import routers
from users.views import SignupUserAPIView, TokenAuthApiView, UserViewSet

app_name = "users"

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

auth_urls = [
    path(r'token/', TokenAuthApiView.as_view()),
    path(r'signup/', SignupUserAPIView.as_view()),
]


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(r'v1/auth/', include(auth_urls)),
]
