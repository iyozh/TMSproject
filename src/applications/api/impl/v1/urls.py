from django.urls import include, path
from rest_framework.routers import DefaultRouter

from applications.api.impl.v1.views import (
    AvatarViewSet,
    PostViewSet,
    TestProjectsViewSet,
)

router = DefaultRouter()

router.register("avatar", AvatarViewSet, "avatar")
router.register("post", PostViewSet, "post")
router.register("test_projects", TestProjectsViewSet, "test_projects")

urlpatterns = [path("", include(router.urls))]
