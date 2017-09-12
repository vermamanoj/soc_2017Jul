from django.contrib import admin

from ServiceNow.models import customer1_incidents

class PessoaAdminModel(admin.ModelAdmin):
    pass

class Cusotmer1IncidentsAdminModel(admin.ModelAdmin):
    pass

admin.site.register(customer1_incidents, Cusotmer1IncidentsAdminModel)


