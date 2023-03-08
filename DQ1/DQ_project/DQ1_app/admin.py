from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import TableA

# Register your models here.

@admin.register(TableA)
class Table5_Info(ImportExportActionModelAdmin):

    class Meta:
        model = TableA
