from django.views.generic import CreateView

from applications.blog.models import Post
from utils.stats_utils import count_stats


@count_stats
class AddPostView(CreateView):
    model = Post
    fields = ["user", "date", "content"]