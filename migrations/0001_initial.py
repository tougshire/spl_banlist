# Generated by Django 5.0.6 on 2024-11-17 23:25

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('spl_members', '0006_alter_jobposition_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bannee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_full', models.CharField(help_text='The name of the bannee', max_length=80, verbose_name='name')),
                ('name_prefered', models.CharField(blank=True, help_text='Nickname, or a name the bannee prefers in place of their first name', max_length=30, verbose_name='prefered name')),
                ('description', models.TextField(blank=True, help_text='A description of the bannee', verbose_name='description')),
            ],
            options={
                'ordering': ('name_full',),
            },
        ),
        migrations.CreateModel(
            name='Banaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='A title for the banaction (ex, Benjamin, three weeks, disruptive behavior )', max_length=255, verbose_name='title')),
                ('banaction_summary', models.TextField(blank=True, help_text='A summary which should include a description of the incident that led to the ban', max_length=255, verbose_name='action summary')),
                ('when_submitted', models.DateField(blank=True, help_text='The date and time that the bannee submitted the request', null=True, verbose_name='date submitted')),
                ('when_lifted', models.DateField(help_text='The date that the banaction is lifted. This is required so use a far-distant date for indefinite bans', verbose_name='when lifted')),
                ('submitter', models.ForeignKey(blank=True, help_text='The staff members who is assigned to this appontment or who did the banaction', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_members.member', verbose_name='staff member')),
                ('bannee', models.ForeignKey(blank=True, help_text='The bannee for  whom the apointment is made', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_banlist.bannee')),
            ],
            options={
                'ordering': ('when_submitted',),
            },
        ),
        migrations.CreateModel(
            name='Banactionnote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateField(default=datetime.date.today, help_text='The effective date of the information in the note ( rather than the date the note was made )', null=True, verbose_name='when')),
                ('content', models.CharField(blank=True, help_text='The text of the note.  Optional if a category is chosen and no other details are necessary.', max_length=125, verbose_name='content')),
                ('banaction', models.ForeignKey(help_text='The banaction to which this note applies', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_banlist.banaction')),
            ],
            options={
                'ordering': ['-when'],
            },
        ),
        migrations.CreateModel(
            name='Banneenote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateField(default=datetime.date.today, help_text='The effective date of the information in the note ( rather than the date the note was made )', null=True, verbose_name='when')),
                ('content', models.CharField(blank=True, help_text='The text of the note.  Optional if a category is chosen and no other details are necessary.', max_length=125, verbose_name='content')),
                ('bannee', models.ForeignKey(help_text='The bannee to which this note applies', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_banlist.bannee')),
            ],
        ),
        migrations.CreateModel(
            name='Banneephoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='An optional title for the photo', max_length=80, verbose_name='title')),
                ('photofile', models.ImageField(upload_to='banlist', verbose_name='photo file')),
                ('when_taken', models.DateField(default=datetime.date.today, help_text='The date in which the photo was taken', null=True, verbose_name='when taken')),
                ('is_primary', models.BooleanField(default=False, help_text='If this is a primary photo for this bannee ', verbose_name='is primary')),
                ('bannee', models.ForeignKey(help_text='The bannee to whom this note applies', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_banlist.bannee')),
            ],
            options={
                'ordering': ['-is_primary', '-when_taken'],
            },
        ),
    ]
