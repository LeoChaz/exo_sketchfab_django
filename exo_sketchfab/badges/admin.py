__author__ = 'leomaltrait'


from django.contrib import admin

from .models import Badges


class BadgesAdmin(admin.ModelAdmin):
    list_display = ('name', )

    class Meta:
        model = Badges


admin.site.register(Badges, BadgesAdmin)
