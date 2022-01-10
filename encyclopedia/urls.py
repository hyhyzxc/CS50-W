from django.urls import path

from . import views
from . import util

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("random", views.random_page, name="random")
]

for entry in util.list_entries():
    urlpatterns.append(path("wiki/<str:entry>", views.display_content, name = f"{entry}"))
   
