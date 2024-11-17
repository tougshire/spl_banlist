from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import views
from django.views.i18n import JavaScriptCatalog

app_name = "spl_banlist"

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url=reverse_lazy("spl_banlist:banaction-list")),
    ),
    path(
        "banaction/",
        RedirectView.as_view(url=reverse_lazy("spl_banlist:banaction-list")),
    ),
    path(
        "banaction/create/",
        views.BanactionCreate.as_view(),
        name="banaction-create",
    ),
    path(
        "banaction/<int:pk>/update/",
        views.BanactionUpdate.as_view(),
        name="banaction-update",
    ),
    path(
        "banaction/<int:pk>/detail/",
        views.BanactionDetail.as_view(),
        name="banaction-detail",
    ),
    path(
        "banaction/<int:pk>/delete/",
        views.BanactionDelete.as_view(),
        name="banaction-delete",
    ),
    path(
        "banaction/list/filterstore/<int:from_store>/",
        views.BanactionList.as_view(),
        name="banaction-filterstore",
    ),
    path(
        "banaction/list/",
        views.BanactionList.as_view(),
        name="banaction-list",
    ),
    path(
        "banaction/<str:copied_from>/copied/",
        views.BanactionList.as_view(),
        name="banaction-copied",
    ),
    path(
        "bannee/",
        RedirectView.as_view(url=reverse_lazy("spl_banlist:bannee-list")),
    ),
    path("bannee/create/", views.BanneeCreate.as_view(), name="bannee-create"),
    path("bannee/popup/", views.BanneeCreate.as_view(), name="bannee-popup"),
    path(
        "bannee/<int:pk>/update/",
        views.BanneeUpdate.as_view(),
        name="bannee-update",
    ),
    path(
        "bannee/<int:pk>/detail/",
        views.BanneeDetail.as_view(),
        name="bannee-detail",
    ),
    path(
        "bannee/<int:pk>/delete/",
        views.BanneeDelete.as_view(),
        name="bannee-delete",
    ),
    path("bannee/list/", views.BanneeList.as_view(), name="bannee-list"),
    path(
        "jsi18n",
        JavaScriptCatalog.as_view(),
        name="js-catlog",
    ),
]
