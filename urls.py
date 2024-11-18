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
        "customer/",
        RedirectView.as_view(url=reverse_lazy("spl_banlist:customer-list")),
    ),
    path("customer/create/", views.CustomerCreate.as_view(), name="customer-create"),
    path("customer/popup/", views.CustomerCreate.as_view(), name="customer-popup"),
    path(
        "customer/<int:pk>/update/",
        views.CustomerUpdate.as_view(),
        name="customer-update",
    ),
    path(
        "customer/<int:pk>/detail/",
        views.CustomerDetail.as_view(),
        name="customer-detail",
    ),
    path(
        "customer/<int:pk>/delete/",
        views.CustomerDelete.as_view(),
        name="customer-delete",
    ),
    path("customer/list/", views.CustomerList.as_view(), name="customer-list"),
    path(
        "jsi18n",
        JavaScriptCatalog.as_view(),
        name="js-catlog",
    ),
]
