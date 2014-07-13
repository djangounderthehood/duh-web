from django.contrib import admin

from .models import Interest

class InterestAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'message', 'created_on')


admin.site.register(Interest, InterestAdmin)
