from django.contrib import admin
from .models import Pergunta, Resposta

# Register your models here.
class RespostaEmLinha(admin.TabularInline): #StackedInline: o campo voto vai embaixo do resposta_text (ocupa mais espaço na tela)
    model = Resposta
    extra = 3

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields':['pergunta_text']}),
        ('Data information', {'fields':['data_publicada'], 'classe':
        ['collapse']}),
    ]
    inlines = [RespostaEmLinha]
    list_display = ('pergunta_text', 'data_publicada', 'foi_publicado_recentemente')
    list_filter = ['data_publicada']
    search_fields = ['pergunta_text']

admin.site.register(Pergunta, PerguntaAdmin)