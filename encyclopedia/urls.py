from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:pagename>", views.get_page, name="get_page"),
    path("search_page/", views.search_page, name="search_page"),
    path("create_page/", views.create_page, name="create_page"),
    path("edit_page/", views.edit_page, name="edit_page"),
    path("save_page/", views.save_page, name="save_page"),
    path("random_page/", views.random_page, name="random_page"),
]
