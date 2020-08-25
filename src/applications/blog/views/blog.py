from django.views.generic import ListView

from applications.blog.models import Post
from utils.stats_utils import count_stats


@count_stats
class BlogView(ListView):
    template_name = "blog/blog.html"
    model = Post