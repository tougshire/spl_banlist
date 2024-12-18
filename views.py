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

from .filterset import BanactionFilter, CustomerFilter
from .forms import (
    BanactionForm,
    CustomerCustomerphotoFormset,
    CustomerCustomernoteFormset,
    CustomerForm,
    CSVOptionForm,
)
from .models import Banaction, Customer

logger = logging.getLogger(__name__)


class BanactionCreate(PermissionRequiredMixin, CreateView):
    permission_required = "spl_banlist.add_banaction"
    model = Banaction
    form_class = BanactionForm
    template_name = "spl_banlist/banaction_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {}

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

        formsetclasses = {}
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

        formsetclasses = {}

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

        formsetclasses = {}
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

        return context_data


class BanactionDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "spl_banlist.delete_banaction"
    model = Banaction
    success_url = reverse_lazy("spl_banlist:banaction-list")

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)
        context_data["banaction_labels"] = make_labels(Banaction)
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

class BanactionCSV(PermissionRequiredMixin, FilterView):

    permission_required = "spl_banlist.view_banaction"
    filterset_class = BanactionFilter
    template_name = "spl_banlist/csv.txt"
    content_type = "text/csv"
    headers = {"Content-Disposition": 'attachment; filename="spl_banlist.csv"'}

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        response.headers = {
            "Content-Disposition": 'attachment; filename="spl_banlist.csv"'
        }
        return response

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        data = [
            [
                "Customer",
                "Summary",
                "Start Date",
                "Expiration",
                "Submitter",
                "Photo",
            ]
        ]
        for banaction in context_data["filter"].qs:
            data.append(
                [
                    banaction.customer,
                    banaction.summary,
                    banaction.start_date,
                    banaction.expiration,
                    banaction.submitter,
                    banaction.get_photo().photofile.url,
                ]
            )
        context_data["data"] = data
        return context_data

class CustomerCreate(PermissionRequiredMixin, CreateView):
    permission_required = "spl_banlist.add_customer"
    model = Customer
    form_class = CustomerForm
    template_name = "spl_banlist/customer_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "customerphotos": CustomerCustomerphotoFormset,
            "customernotes": CustomerCustomernoteFormset,
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
            "customerphotos": CustomerCustomerphotoFormset,
            "customernotes": CustomerCustomernoteFormset,

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
            "spl_banlist:customer-detail", kwargs={"pk": self.object.pk}
        )


class CustomerUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "spl_banlist.change_customer"
    model = Customer
    form_class = CustomerForm
    template_name = "spl_banlist/customer_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "customerphotos": CustomerCustomerphotoFormset,
            "customernotes": CustomerCustomernoteFormset,

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
            "customerphotos": CustomerCustomerphotoFormset,
            "customernotes": CustomerCustomernoteFormset,
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
            "spl_banlist:customer-detail", kwargs={"pk": self.object.pk}
        )


class CustomerDetail(PermissionRequiredMixin, DetailView):
    permission_required = "spl_banlist.view_customer"
    model = Customer

    def get_context_data(self, **kwargs):

        print ('tp24bfi02', self.get_object().customerphoto_set.all())

        context_data = super().get_context_data(**kwargs)

        context_data["customer_labels"] = make_labels(Customer)

        return context_data


class CustomerDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "spl_banlist.delete_customer"
    model = Customer
    success_url = reverse_lazy("spl_banlist:customer-list")


class CustomerList(PermissionRequiredMixin, FilterView):
    permission_required = "spl_banlist.view_customer"
    filterset_class = CustomerFilter
    filterstore_urlname = "spl_banlist:customer-filterstore"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()
        context_data["count"] = self.object_list.count()
        context_data["labels"] = make_labels(Customer)
        return context_data


