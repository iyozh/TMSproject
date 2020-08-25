
from django.views.generic import DetailView

from applications.blog.models import Post





class PostView(DetailView):
    template_name = "blog/post.html"
    model = Post