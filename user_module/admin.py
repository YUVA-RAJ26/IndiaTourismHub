from django.contrib import admin
from .models import Users, Booking, Invoice

# Register your models here.
admin.site.register(Users)
admin.site.register(Booking)
admin.site.register(Invoice)