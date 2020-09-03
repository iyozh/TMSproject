from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.blog.models import Post
from applications.blog.views.blog import PostForm
from utils.stats_utils import count_stats


@count_stats
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy("blog:blog")

    def form_valid(self, form):
        user_id = form.data["user"]
        post = Post(profile_id=user_id,content=form.cleaned_data["content"])
        post.save()
        return super().form_valid(form)