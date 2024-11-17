from django import forms
from django.forms import inlineformset_factory
from django.urls import reverse_lazy

from spl_members.models import Member as Staffmember
from touglates.widgets import TouglatesRelatedSelect
from .models import Banaction, Banactionnote, Bannee, Banneenote, Banneephoto
from django.contrib.admin.widgets import AdminDateWidget


class CSVOptionForm(forms.Form):

    make_csv = forms.BooleanField(
        label="CSV",
        initial=False,
        required=False,
        help_text="Download the result as a CSV file",
    )


class BanactionForm(forms.ModelForm):
    class Meta:
        model = Banaction
        fields = [
            "title",
            "bannee",
            "banaction_summary",
            "when_submitted",
            "submitter",
            "when_lifted",
        ]
        widgets = {
            "bannee": TouglatesRelatedSelect(
                related_data={
                    "model_name": "Bannee",
                    "app_name": "spl_banlist",
                    "add_url": reverse_lazy("spl_banlist:bannee-popup"),
                },
            ),
            "staffer": TouglatesRelatedSelect(
                related_data={
                    "app_name": "spl_members",
                    "model_name": "Member",
                    "add_url": reverse_lazy("spl_banlist:staffer-popup"),
                },
            ),
            "when_submitted": AdminDateWidget(),
            "when_lifted": AdminDateWidget(),
        }


class BanactionnoteForm(forms.ModelForm):
    class Meta:
        model = Banactionnote
        fields = ["banaction", "when", "content"]


class BanneeForm(forms.ModelForm):
    class Meta:
        model = Bannee
        fields = [
            "name_full",
            "name_prefered",
            "description",
        ]



class BanneenoteForm(forms.ModelForm):
    class Meta:
        model = Banneenote
        fields = ["bannee", "when", "content"]


class BanneephotoForm(forms.ModelForm):
    class Meta:
        fields=[
            "title",
            "bannee",
            "photofile",
            "when_taken",
        ]

BanactionBanactionnoteFormset = inlineformset_factory(
    Banaction, Banactionnote, form=BanactionnoteForm, extra=10
)
BanneeBanneephotoFormset = inlineformset_factory(
    Bannee, Banneephoto, form=BanneephotoForm, extra=10
)
