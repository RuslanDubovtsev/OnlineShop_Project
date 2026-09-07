from django.contrib import admin
from .models import Vendor, Buyer, Profile, Order

admin.site.register(Vendor)
admin.site.register(Buyer)
admin.site.register(Profile)
admin.site.register(Order)
