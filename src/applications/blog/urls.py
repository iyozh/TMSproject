from django.urls import path


from applications.blog.apps import BlogConfig
from applications.blog.views import BlogView, AddPostView
from applications.blog.views.delete import DeletePostView
from applications.blog.views.update import EditPostView
from applications.blog.views.post import PostView

app_name = BlogConfig.label

urlpatterns = [
    path("", BlogView.as_view(), name="blog"),
    path("add/", AddPostView.as_view(),name="add"),
    path("post/<str:pk>/",PostView.as_view(),name="post"),
    path("post/<str:pk>/edit",EditPostView.as_view(),name="edit"),
    path("post/<str:pk>/delete",DeletePostView.as_view(),name="delete")
]
