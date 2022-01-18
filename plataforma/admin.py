from django.contrib import admin
from .models import *

@admin.register(Imovei)
class ImoveiAdmin(admin.ModelAdmin):
    list_display = ('rua', 'valor', 'quartos', 'tamanho', 'cidade', 'tipo')
    list_editable = ('valor', 'tipo')
    list_filter = ('rua', 'valor', 'quartos', 'tamanho', 'cidade', 'tipo')

admin.site.register(Cidade)
admin.site.register(DiasVisita)
admin.site.register(Horario)
admin.site.register(Imagem)

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('imovel','usuario','dia','horario','status')
    list_editable = ('dia','horario', 'status')
    list_filter = ('imovel','usuario','dia','horario','status')