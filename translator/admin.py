from django.contrib import admin

# Register your models here.
from .models import Wordlist, Translations

admin.site.register(Wordlist)
admin.site.register(Translations)