from django.contrib import admin
from .models import Processo
from .models import Projeto

# -------------------------------------------------------------------
# 1) Formulário padrão para o Admin (sem matrícula/senha)
# -------------------------------------------------------------------
from django import forms

class ProcessoAdminForm(forms.ModelForm):
    class Meta:
        model = Processo
        # Aqui você inclui apenas os campos 'oficiais' do modelo.
        # Como não vamos pedir matrícula/senha no admin, 
        # omitimos totalmente esses campos.
        fields = [ f.name for f in Processo._meta.fields if f.name not in ('rubrica', 'rubrica_montador') ] + [
            # depois você pode querer expor rubrica e rubrica_montador mesmo assim:
            'rubrica', 'rubrica_montador',
        ]

# -------------------------------------------------------------------
# 2) ModelAdmin que usa o form acima
# -------------------------------------------------------------------
@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    # aqui o Django inclui TODOS os campos de Processo, sem precisar listar
    list_display = ('projeto', 'programa', 'rubrica', 'rubrica_montador')
    list_filter  = ('rubrica', 'rubrica_montador')
    search_fields= ('projeto__id', 'programa')

# Se quiser também customizar o Projeto:
@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('id', 'maquina', 'data', 'esta_concluido')
    search_fields= ('maquina',)