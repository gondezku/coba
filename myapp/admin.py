from django.contrib import admin
from .models import Profile, member, site, Open_ticket,ticket_stat,Downtime

# Register your models here.
admin.site.register(Profile)
admin.site.register(member)
admin.site.register(site)
admin.site.register(Open_ticket)
admin.site.register(ticket_stat)
admin.site.register(Downtime)