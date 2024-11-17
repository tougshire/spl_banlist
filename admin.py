from django.contrib import admin

from .models import Banaction,Banactionnote,Bannee,Banneenote

for model in [Banaction,Banactionnote,Bannee,Banneenote]:
    admin.site.register(model)
