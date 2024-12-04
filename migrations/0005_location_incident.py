# Generated by Django 5.0.6 on 2024-11-24 22:47

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spl_banlist', '0004_alter_banaction_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_full', models.CharField(help_text='The full name of the location', max_length=40, verbose_name='location name')),
                ('name_abbr', models.CharField(help_text='An abbreviation of the name', max_length=5, verbose_name='abbreviated name')),
            ],
            options={
                'ordering': ('name_full',),
            },
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(blank=True, help_text='A summary of the incident', max_length=255, verbose_name='summary')),
                ('when', models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time of the incident', verbose_name='date/time')),
                ('customer', models.ForeignKey(blank=True, help_text='The customer involved in this incident', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_banlist.customer')),
                ('submitter', models.ForeignKey(blank=True, help_text='The user who entered this information', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incident', to=settings.AUTH_USER_MODEL, verbose_name='submitter')),
                ('location', models.ForeignKey(blank=True, help_text='The location of the incident', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_banlist.location')),
            ],
            options={
                'ordering': ('-when',),
            },
        ),
    ]
