from datetime import date
from django.db import models
from spl_members.models import Member as Staffmember
from django.utils.timezone import now

class Bannee(models.Model):
    name_full = models.CharField(
        "name", max_length=80, help_text="The name of the bannee"
    )
    name_prefered = models.CharField(
        "prefered name",
        max_length=30,
        blank=True,
        help_text="Nickname, or a name the bannee prefers in place of their first name",
    )
    description = models.TextField(
        "description",
        blank=True,
        help_text="A description of the bannee"
    )

    def banned_until(self):
        active_bans = Banaction.objects.filter(bannee=self,when_lifted__gt=now().date()).order_by("-when_lifted")
        if active_bans.exists():
            return active_bans.first().when_lifted
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
        help_text="A title for the banaction (ex, Benjamin, three weeks, disruptive behavior )",
    )
    bannee = models.ForeignKey(
        Bannee,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The bannee for  whom the apointment is made",
    )
    banaction_summary = models.TextField(
        "action summary",
        blank=True,
        max_length=255,
        help_text="A summary which should include a description of the incident that led to the ban",
    )
    when_submitted = models.DateField(
        "date submitted",
        blank=True,
        null=True,
        help_text="The date and time that the bannee submitted the request",
    )
    submitter = models.ForeignKey(
        Staffmember,
            verbose_name="staff member",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The staff members who is assigned to this appontment or who did the banaction",
    )
    when_lifted = models.DateField(
        "when lifted",
        help_text="The date that the banaction is lifted. This is required so use a far-distant date for indefinite bans",
    )

    def __str__(self):
        ordering = self.when_submitted
        if self.title:
            return self.title
        else:
            return "{}: {}: {}".format(
                self.bannee, self.when_lifted, self.banaction_summary
            )

    class Meta:
        ordering = ("when_submitted",)


class Banactionnote(models.Model):

    banaction = models.ForeignKey(
        Banaction,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The banaction to which this note applies",
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

    class Meta:
        ordering = [
            "-when",
        ]


class Banneephoto(models.Model):

    title = models.CharField(
        "title",
        blank=True,
        max_length=80,
        help_text="An optional title for the photo"
    )
    bannee = models.ForeignKey(
        Bannee,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The bannee to whom this note applies",
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
        help_text="If this is a primary photo for this bannee "
    )

    def __str__(self):
        if self.title:
            return self.title
        else:
            return '{} - {}'.format(self.bannee, self.when_taken.isoformat())

    class Meta:
        ordering = [
            "-is_primary",
            "-when_taken",
        ]

class Banneenote(models.Model):
    bannee = models.ForeignKey(
        Bannee,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The bannee to which this note applies",
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
