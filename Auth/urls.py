from django.conf.urls import url

from . import views

app_name = "auth"
urlpatterns = [
    url(r'^login/$', views.user_login, name="user_login"),
    url(r"^regist/$", views.register, name="user_regist"),
    url(r'^regist2/$', views.register_pro, name="user_regist2"),
    url(r'^editinfo/$', views.editInfo, name="edit_myself"),
    url(r"^showinfo/$", views.showInfo, name="show_info")
]

