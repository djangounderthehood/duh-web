from django.contrib import admin

from .models import Sponsor


def make_live(modeladmin, request, queryset):
    queryset.update(is_live=True)

make_live.short_description = "Show selected sponsor(s) on homepage"


def undo_live(modeladmin, request, queryset):
    queryset.update(is_live=False)

undo_live.short_description = "Hide selected sponsor(s) on homepage"


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('level', 'name', 'is_live')
    list_filter = ('level', 'is_live')

    actions = [make_live, undo_live]


admin.site.register(Sponsor, SponsorAdmin)
