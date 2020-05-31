from django.contrib import admin
from .models import Hospital, Ambiente, Respirador
# Register your models here.

class RespiradorAdmin(admin.ModelAdmin):
    pass

class AmbienteAdmin(admin.ModelAdmin):
    pass

class HospitalAdmin(admin.ModelAdmin):
    pass

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Respirador, RespiradorAdmin)
admin.site.register(Ambiente, AmbienteAdmin)