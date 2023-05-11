from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APIToken, APISignup, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet)

app_name = 'api'

router = SimpleRouter()

router.register(
    'users',
    UsersViewSet,
    basename='users'
)


urlpatterns = [
    path('v1/auth/token/', APIToken.as_view(), name='api_token'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='api_signup'),
]