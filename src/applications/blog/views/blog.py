from django import forms
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from applications.blog.models import Post
from utils.stats_utils import count_stats


class PostForm(forms.ModelForm):
    class Meta:
        fields = [Post.content.field.name]
        labels = {Post.content.field.name: "Say something..."}
        model = Post
        widgets = {
            Post.content.field.name: forms.Textarea(attrs={"cols": 70, "rows": 2}),
        }

@count_stats
class BlogView(FormMixin, ListView):
    template_name = "blog/blog.html"
    form_class = PostForm
    model = Post
