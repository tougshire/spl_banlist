from django.http import QueryDict
import django_filters

from django_filters_stoex.filterset import StoexFilterSet
from spl_members.models import Member as Staffmember
from .models import Banaction, Bannee
from django.db import models
from django import forms
from django_filters_stoex.filters import CrossFieldSearchFilter,ExpandedDateRangeFilter
from touglates.widgets import DropdownSelectMultiple


class BanactionFilter(StoexFilterSet):

    combined_text_search = CrossFieldSearchFilter(
        label="Text Search",
        field_name="title,bannee__name_full,bannee__name_prefered,banaction_summary,submitter__name_full",
        lookup_expr="icontains",
    )
    bannee = django_filters.ModelMultipleChoiceFilter(
        widget=DropdownSelectMultiple,
        field_name="bannee",
        label="Bannee",
        queryset=Bannee.objects.all(),
    )
    banaction_summary = django_filters.CharFilter(
        field_name="banaction_summary",
        label="Summary",
        initial="Test"
    )
    when_lifted = ExpandedDateRangeFilter(
        field_name="when_lifted",
        help_text="Select \"After Today\" for currently active bans"
    )
    orderbyfields = django_filters.OrderingFilter(
        fields=(
            "when_lifted",
            "when_submitted",
            "bannee",
            "staffer",
        ),
    )

    class Meta:
        model = Banaction
        fields = []


class BanneeFilter(StoexFilterSet):

    name_search = CrossFieldSearchFilter(
        label="Text Search",
        field_name="name_full, name_prefered",
        lookup_expr="icontains",
    )
    banaction__when_lifted = ExpandedDateRangeFilter(
        field_name="banaction__when_lifted",
        label="Ban Lift Date",
        help_text="Select \"After Today\" for currently active bans"
    )

    orderbyfields = django_filters.OrderingFilter(
        fields=(
            "when_lifted",
            "name_prefered",
            "name_full",
        ),
    )

    class Meta:
        model = Bannee
        fields = []
