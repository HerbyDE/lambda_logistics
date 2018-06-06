from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission


# Register your models here.

admin.site.register(Parcel)
admin.site.register(Permission)
admin.site.register(Office)