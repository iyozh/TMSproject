from rest_framework.serializers import ModelSerializer

from applications.blog.models import Post
from applications.onboarding.models import Avatar
from applications.test_projects.models import Project


class AvatarSerializer(ModelSerializer):
    class Meta:
        model = Avatar
        fields = "__all__"


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class TestProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
