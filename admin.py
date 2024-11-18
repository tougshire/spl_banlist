from django.contrib import admin

from .models import Banaction,Customer,Customernote

for model in [Banaction,Customer,Customernote]:
    admin.site.register(model)
