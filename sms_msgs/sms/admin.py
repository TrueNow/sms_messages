from django.contrib import admin
from . import models


class ClientAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'timezone',)
    list_filter = ('operator_code', 'tag',)
    ordering = ('phone_number',)


class MailingAdmin(admin.ModelAdmin):
    list_display = (models.Mailing.__str__, 'date_start', 'date_end')
    list_filter = ('date_start', 'date_end')


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Mailing, MailingAdmin)
admin.site.register(models.Message)
