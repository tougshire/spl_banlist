from datetime import date, timedelta
from django.db import models
from spl_members.models import Member as Staffmember
from django.utils.timezone import now
from django.conf import settings

def seven_days_hence():
    return now() + timedelta(days=7)

class Customer(models.Model):
    name_full = models.CharField(
        "name", max_length=80, help_text="The name of the customer"
    )
    name_prefered = models.CharField(
        "prefered name",
        max_length=30,
        blank=True,
        help_text="Nickname, or a name the customer prefers in place of their first name",
    )
    description = models.TextField(
        "description",
        blank=True,
        help_text="A description of the customer"
    )

    def banned_until(self):
        active_bans = Banaction.objects.filter(customer=self,expiration__gt=now().date()).order_by("-expiration")
        if active_bans.exists():
            return active_bans.first().expiration
        return None

    def __str__(self):
        return self.name_full

    class Meta:
        ordering = ("name_full",)

class Banaction(models.Model):

    title = models.CharField(
        "title",
        max_length=255,
        blank=True,
        help_text="A title for the ban (ex, Benjamin, three weeks, disruptive behavior ).  This is optional. The date and customer's name will be used if left blank",
    )
    customer = models.ForeignKey(
        Customer,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The customer for whom the ban is applies",
    )
    summary = models.TextField(
        "summary",
        blank=True,
        max_length=255,
        help_text="A summary which should include a description of the incident that led to the ban",
    )
    start_date = models.DateField(
        "start date",
        default=date.today,
        help_text="The date and time that the ban began or will begin",
    )
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="submitter",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The user who entered this information",
    )
    expiration = models.DateField(
        "expiration",
        default=seven_days_hence,
        help_text="The date as of which the customer is no longer banned. For an indefinite ban, set the date far in the future (ie ten years)",
    )
    def is_expired(self):
        if self.expiration > now().date():
            return False
        return True

    def get_photo(self):
        try:
            return self.customer.customerphoto_set.first()
        except:
            return None

    def __str__(self):
        ordering = self.start_date
        if self.title:
            return self.title
        else:
            return "{} until {} {}".format(
                self.customer, self.expiration, '(expired)' if self.is_expired() else ""
            )

    class Meta:
        ordering = ("-expiration",)


class Customerphoto(models.Model):

    title = models.CharField(
        "title",
        blank=True,
        max_length=80,
        help_text="An optional title for the photo"
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The customer to whom this note applies",
    )
    photofile = models.ImageField(
        "photo file",
        upload_to="banlist",
    )
    when_taken = models.DateField(
        "when taken",
        null=True,
        default=date.today,
        help_text="The date in which the photo was taken",
    )
    is_primary = models.BooleanField(
        "is primary",
        default=False,
        help_text="If this is a primary photo for this customer "
    )

    def __str__(self):
        if self.title:
            return self.title
        else:
            return '{} - {}'.format(self.customer, self.when_taken.isoformat())

    class Meta:
        ordering = [
            "-is_primary",
            "-when_taken",
        ]

class Customernote(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The customer to which this note applies",
    )
    when = models.DateField(
        "when",
        null=True,
        default=date.today,
        help_text="The effective date of the information in the note ( rather than the date the note was made )",
    )
    content = models.CharField(
        "content",
        max_length=125,
        blank=True,
        help_text="The text of the note.  Optional if a category is chosen and no other details are necessary.",
    )

    def __str__(self):
        str = self.when.isoformat() + ": "
        if self.content:
            str = str + self.content + ": "
        if len(str) > 2:
            str = str[0:-2]
        if len(str) > 50:
            str = str[0:45] + " ..."

        return str
