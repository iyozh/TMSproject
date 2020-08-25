from django.views.generic import UpdateView

from applications.blog.models import Post


class EditPostView(UpdateView):
    model = Post
    fields = ["user","date","content"]
    template_name_suffix = '_update_form'