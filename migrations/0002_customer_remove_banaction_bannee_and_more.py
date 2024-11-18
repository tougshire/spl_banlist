# Generated by Django 5.0.6 on 2024-11-18 10:08

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spl_banlist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_full', models.CharField(help_text='The name of the customer', max_length=80, verbose_name='name')),
                ('name_prefered', models.CharField(blank=True, help_text='Nickname, or a name the customer prefers in place of their first name', max_length=30, verbose_name='prefered name')),
                ('description', models.TextField(blank=True, help_text='A description of the customer', verbose_name='description')),
            ],
            options={
                'ordering': ('name_full',),
            },
        ),
        migrations.RemoveField(
            model_name='banaction',
            name='bannee',
        ),
        migrations.RemoveField(
            model_name='banneephoto',
            name='bannee',
        ),
        migrations.AlterField(
            model_name='banaction',
            name='when_submitted',
            field=models.DateField(blank=True, help_text='The date and time that the customer submitted the request', null=True, verbose_name='date submitted'),
        ),
        migrations.AddField(
            model_name='banaction',
            name='customer',
            field=models.ForeignKey(blank=True, help_text='The customer for  whom the apointment is made', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_banlist.customer'),
        ),
        migrations.CreateModel(
            name='Customernote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateField(default=datetime.date.today, help_text='The effective date of the information in the note ( rather than the date the note was made )', null=True, verbose_name='when')),
                ('content', models.CharField(blank=True, help_text='The text of the note.  Optional if a category is chosen and no other details are necessary.', max_length=125, verbose_name='content')),
                ('customer', models.ForeignKey(help_text='The customer to which this note applies', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_banlist.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Customerphoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='An optional title for the photo', max_length=80, verbose_name='title')),
                ('photofile', models.ImageField(upload_to='banlist', verbose_name='photo file')),
                ('when_taken', models.DateField(default=datetime.date.today, help_text='The date in which the photo was taken', null=True, verbose_name='when taken')),
                ('is_primary', models.BooleanField(default=False, help_text='If this is a primary photo for this customer ', verbose_name='is primary')),
                ('customer', models.ForeignKey(help_text='The customer to whom this note applies', null=True, on_delete=django.db.models.deletion.SET_NULL, to='spl_banlist.customer')),
            ],
            options={
                'ordering': ['-is_primary', '-when_taken'],
            },
        ),
        migrations.DeleteModel(
            name='Banneenote',
        ),
        migrations.DeleteModel(
            name='Bannee',
        ),
        migrations.DeleteModel(
            name='Banneephoto',
        ),
    ]
