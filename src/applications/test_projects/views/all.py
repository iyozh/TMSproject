from django import forms
from django.views.generic import ListView


from applications.test_projects.models import Project
from utils.stats_utils import count_stats


class Search(forms.Form):
    search = forms.CharField(max_length=50,required=False,label="",widget=forms.TextInput(attrs={'placeholder': 'Search...'}))



@count_stats
class TestProjectsView(ListView):
    template_name = "test_projects/projects_template.html"
    queryset = Project.objects.filter(visible=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx["form"] = Search(self.request.GET)
        return ctx

    def get_queryset(self):
        qs = Project.objects.all()
        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            qs = qs.filter(name=search)
        return qs



