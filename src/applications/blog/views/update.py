from django.urls import reverse_lazy
from django.views.generic import UpdateView

from applications.blog.models import Post
from applications.blog.views.post import UpdatePostForm


class EditPostView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    http_method_names = ["post"]
