from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.edit import FormMixin

from applications.blog.models import Post


class DeletePostView(DeleteView):
    success_url = reverse_lazy("blog:blog")
    model = Post
    http_method_names = ["post"]
