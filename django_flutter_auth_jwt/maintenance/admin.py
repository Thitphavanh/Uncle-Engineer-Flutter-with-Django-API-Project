from django.contrib import admin
from .models import Maintenance


class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ["name", "department", "machine"]


admin.site.register(Maintenance, MaintenanceAdmin)
