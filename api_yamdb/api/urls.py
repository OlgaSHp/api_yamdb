from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    APISignup,
    APIToken,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UsersViewSet,
)

app_name = "api"

router = DefaultRouter()

router.register(r"users", UsersViewSet)
router.register("categories", CategoryViewSet, basename="сategories")
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet, basename="genres")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/auth/token/", APIToken.as_view(), name="api_token"),
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", APISignup.as_view(), name="api_signup"),
]
