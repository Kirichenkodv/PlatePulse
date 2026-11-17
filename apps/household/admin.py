from django.contrib import admin

from .models import HouseHold, HouseHoldInvite

# admin.register(HouseHold, HouseHoldInvite)
admin.site.register(HouseHold)
admin.site.register(HouseHoldInvite)
