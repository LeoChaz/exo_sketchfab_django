__author__ = 'leomaltrait'


from django.contrib import admin

from .models import Model3d


class Model3dAdmin(admin.ModelAdmin):
    list_display = ('model3d_owner', 'name', 'date_added', 'view_count')

    class Meta:
        model = Model3d


admin.site.register(Model3d, Model3dAdmin)