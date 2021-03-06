from django import forms
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from applications.blog.models import Post
from utils.stats_utils import count_stats


class UpdatePostForm(forms.ModelForm):
    class Meta:
        fields = [Post.content.field.name]
        labels = {Post.content.field.name: "Edit your post"}
        model = Post
        widgets = {
            Post.content.field.name: forms.Textarea(attrs={"cols": 70, "rows": 2}),
        }


@count_stats
class PostView(FormMixin, DetailView):
    template_name = "blog/post.html"
    model = Post
    form_class = UpdatePostForm

    def get_initial(self):
        return {Post.content.field.name: self.object.content}
