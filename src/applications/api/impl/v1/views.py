from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from applications.api.impl.v1.serializers import (
    AvatarSerializer,
    PostSerializer,
    TestProjectsSerializer,
)
from applications.blog.models import Post
from applications.onboarding.models import Avatar
from applications.test_projects.models import Project


class AvatarViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AvatarSerializer
    queryset = Avatar.objects.all()


class PostViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class TestProjectsViewSet(ReadOnlyModelViewSet):
    serializer_class = TestProjectsSerializer
    queryset = Project.objects.all()
