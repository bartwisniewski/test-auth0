from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path("entries/", views.EntryListView.as_view(), name="entries"),
    path("entry/<pk>", views.EntryDetailView.as_view(), name="entry"),
    path("create/", views.EntryCreateView.as_view(), name="entry-create"),
]
