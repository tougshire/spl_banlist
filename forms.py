from django import forms
from django.forms import inlineformset_factory
from django.urls import reverse_lazy

from spl_members.models import Member as Staffmember
from touglates.widgets import TouglatesRelatedSelect
from .models import Banaction, Banactionnote, Customer, Customernote, Customerphoto
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
            "customer",
            "banaction_summary",
            "when_submitted",
            "submitter",
            "when_lifted",
        ]
        widgets = {
            "customer": TouglatesRelatedSelect(
                related_data={
                    "model_name": "Customer",
                    "app_name": "spl_banlist",
                    "add_url": reverse_lazy("spl_banlist:customer-popup"),
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


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name_full",
            "name_prefered",
            "description",
        ]



class CustomernoteForm(forms.ModelForm):
    class Meta:
        model = Customernote
        fields = ["customer", "when", "content"]


class CustomerphotoForm(forms.ModelForm):
    class Meta:
        fields=[
            "title",
            "customer",
            "photofile",
            "when_taken",
        ]

BanactionBanactionnoteFormset = inlineformset_factory(
    Banaction, Banactionnote, form=BanactionnoteForm, extra=10
)
CustomerCustomerphotoFormset = inlineformset_factory(
    Customer, Customerphoto, form=CustomerphotoForm, extra=10
)
