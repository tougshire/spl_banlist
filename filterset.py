from django.http import QueryDict
import django_filters

from django_filters_stoex.filterset import StoexFilterSet
from .models import Banaction, Customer
from django.db import models
from django import forms
from django_filters_stoex.filters import CrossFieldSearchFilter,ExpandedDateRangeFilter
from touglates.widgets import DropdownSelectMultiple


class BanactionFilter(StoexFilterSet):

    combined_text_search = CrossFieldSearchFilter(
        label="Text Search",
        field_name="title,customer__name_full,customer__name_prefered,summary",
        lookup_expr="icontains",
    )
    customer = django_filters.ModelMultipleChoiceFilter(
        widget=DropdownSelectMultiple,
        field_name="customer",
        label="Customer",
        queryset=Customer.objects.all(),
    )
    summary = django_filters.CharFilter(
        field_name="summary",
        label="Summary",
        initial="Test"
    )
    expiration = ExpandedDateRangeFilter(
        field_name="expiration",
        help_text="Select \"After Today\" for currently active bans"
    )
    orderbyfields = django_filters.OrderingFilter(
        fields=(
            "expiration",
            "start_date",
            "customer",
            "staffer",
        ),
    )

    class Meta:
        model = Banaction
        fields = []


class CustomerFilter(StoexFilterSet):

    name_search = CrossFieldSearchFilter(
        label="Text Search",
        field_name="name_full, name_prefered",
        lookup_expr="icontains",
    )
    banaction__expiration = ExpandedDateRangeFilter(
        field_name="banaction__expiration",
        label="Ban Lift Date",
        help_text="Select \"After Today\" for currently active bans"
    )

    orderbyfields = django_filters.OrderingFilter(
        fields=(
            "name_prefered",
            "name_full",
        ),
    )

    class Meta:
        model = Customer
        fields = []
