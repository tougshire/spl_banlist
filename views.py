import csv
import logging
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import QueryDict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView

from django_filters_stoex.forms import FilterstoreRetrieveForm, FilterstoreSaveForm
from django_filters_stoex.views import FilterView
from spl_members.models import Member as Staffmember
from touglates.views import make_labels

from .filterset import BanactionFilter, BanneeFilter
from .forms import (
    BanactionBanactionnoteFormset,
    BanactionForm,
    BanneeBanneephotoFormset,
    BanneeForm,
)
from .models import Banaction, Banactionnote, Bannee

logger = logging.getLogger(__name__)


class BanactionCreate(PermissionRequiredMixin, CreateView):
    permission_required = "spl_banlist.add_banaction"
    model = Banaction
    form_class = BanactionForm
    template_name = "spl_banlist/banaction_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "banactionnotes": BanactionBanactionnoteFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        banaction_labels = make_labels(Banaction)

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "banactionnotes": BanactionBanactionnoteFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy(
            "spl_banlist:banaction-detail", kwargs={"pk": self.object.pk}
        )

    def form_invalid(self, form):

        return super().form_invalid(form)

class BanactionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "spl_banlist.change_banaction"
    model = Banaction
    form_class = BanactionForm
    template_name = "spl_banlist/banaction_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "banactionnotes": BanactionBanactionnoteFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                context_data[formsetkey] = formsetclass(instance=self.object)

        banaction_labels = make_labels(Banaction)

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save()

        formsetclasses = {
            "banactionnotes": BanactionBanactionnoteFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        if "popup" in self.kwargs:
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy(
            "spl_banlist:banaction-detail", kwargs={"pk": self.object.pk}
        )


class BanactionDetail(PermissionRequiredMixin, DetailView):
    permission_required = "spl_banlist.view_banaction"
    model = Banaction

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["banaction_labels"] = make_labels(Banaction)

        context_data["banactionnote_labels"] = make_labels(Banactionnote)

        return context_data


class BanactionDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "spl_banlist.delete_banaction"
    model = Banaction
    success_url = reverse_lazy("spl_banlist:banaction-list")

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)
        context_data["banaction_labels"] = make_labels(Banaction)
        print("tp23be625", context_data["banaction_labels"])
        context_data["banactionnote_labels"] = make_labels(Banactionnote)
        return context_data

class BanactionList(PermissionRequiredMixin, FilterView):
    permission_required = "spl_banlist.view_banaction"
    filterset_class = BanactionFilter
    filterstore_urlname = "spl_banlist:banaction-filterstore"
    model=Banaction


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()
        context_data["count"] = self.object_list.count()
        context_data["appoitment_labels"] = make_labels(Banaction)
        return context_data

class BanactionClose(PermissionRequiredMixin, DetailView):
    permission_required = "spl_banlist.view_banaction"
    model = Banaction
    template_name = "spl_banlist/banaction_closer.html"


class BanneeCreate(PermissionRequiredMixin, CreateView):
    permission_required = "spl_banlist.add_bannee"
    model = Bannee
    form_class = BanneeForm
    template_name = "spl_banlist/bannee_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "banneephotos": BanneeBanneephotoFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "banneephotos": BanneeBanneephotoFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, self.request.FILES, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy(
            "spl_banlist:bannee-detail", kwargs={"pk": self.object.pk}
        )


class BanneeUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "spl_banlist.change_bannee"
    model = Bannee
    form_class = BanneeForm
    template_name = "spl_banlist/bannee_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "banneephotos": BanneeBanneephotoFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                context_data[formsetkey] = formsetclass(instance=self.object)

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save()

        formsetclasses = {
            "banneephotos": BanneeBanneephotoFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, self.request.FILES, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        if "popup" in self.kwargs:
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy(
            "spl_banlist:bannee-detail", kwargs={"pk": self.object.pk}
        )


class BanneeDetail(PermissionRequiredMixin, DetailView):
    permission_required = "spl_banlist.view_bannee"
    model = Bannee

    def get_context_data(self, **kwargs):

        print ('tp24bfi02', self.get_object().banneephoto_set.all())

        context_data = super().get_context_data(**kwargs)

        context_data["bannee_labels"] = make_labels(Bannee)

        return context_data


class BanneeDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "spl_banlist.delete_bannee"
    model = Bannee
    success_url = reverse_lazy("spl_banlist:bannee-list")


class BanneeList(PermissionRequiredMixin, FilterView):
    permission_required = "spl_banlist.view_bannee"
    filterset_class = BanneeFilter
    filterstore_urlname = "spl_banlist:bannee-filterstore"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()
        context_data["count"] = self.object_list.count()
        context_data["labels"] = make_labels(Bannee)
        return context_data


