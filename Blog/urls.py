from django.conf.urls import url
from . import views

namespace = "article"
urlpatterns = [
   url(r'^article-column/$', views.article_column, name="article_column"),
   url(r'^exit-column/$', views.exit_column, name="exit_column"),
   url(r'^add-post/$', views.add_post, name="add_post"),
   url(r'^article-list/$', views.article_list, name="article_list"),
   url(r"^show-article/(?P<pid>\d+)/(?P<slug>[-\w]+)/$", views.article_detail, name="show_article")
]
