from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.blog.models import Post
from applications.blog.views.blog import PostForm
from utils.stats_utils import count_stats


class MyLoginRequiredMixin(LoginRequiredMixin):
    def get_next_url(self):
        return self.request.get_full_path()

    def handle_no_permission(self):
        next_url = self.get_next_url()

        previous_meth = self.request.get_full_path
        self.request.get_full_path = lambda: next_url

        try:
            r = super().handle_no_permission()
            return r
        finally:
            self.request.get_full_path = previous_meth


@count_stats
class AddPostView(MyLoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    http_method_names = ["post"]
    next_url = reverse_lazy("blog:blog")
    success_url = reverse_lazy("blog:blog")

    def get_next_url(self):
        form = self.form_class(self.request.POST)
        content = form.data["content"]
        redirect = reverse_lazy("blog:blog")
        return f"{redirect}?content={content}"

    def form_valid(self, form):
        redirect_response = super().form_valid(form)
        user_id = form.data.get("user")
        self.object.user_id = user_id
        self.object.save()
        return redirect_response
