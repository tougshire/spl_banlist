from django.contrib import admin

from .models import Banaction,Banactionnote,Customer,Customernote

for model in [Banaction,Banactionnote,Customer,Customernote]:
    admin.site.register(model)
