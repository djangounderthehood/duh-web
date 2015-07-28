from django.contrib import admin

from .models import Sponsor


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('level', 'name', 'is_live')
    list_filter = ('level', 'is_live')


admin.site.register(Sponsor, SponsorAdmin)
