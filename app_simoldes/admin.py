from django.contrib import admin
from .models import *
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

from .models import Processo

admin.site.register(Projeto)
admin.site.register(Processo)

class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'rubrica', 'rubrica_montador', ...)
    # ... qualquer outra configuração do admin

    def save_model(self, request, obj, form, change):
        # Se for edição (change=True), verifica mudanças nesses campos
        if change:
            # carrega o objeto anterior do banco
            antigo = Processo.objects.get(pk=obj.pk)

            if antigo.rubrica != obj.rubrica:
                LogEntry.objects.log_action(
                    user_id         = request.user.pk,
                    content_type_id = ContentType.objects.get_for_model(obj).pk,
                    object_id       = obj.pk,
                    object_repr     = str(obj),
                    action_flag     = CHANGE,
                    change_message  = f"rubrica mudou de {antigo.rubrica} para {obj.rubrica}",
                )

            if antigo.rubrica_montador != obj.rubrica_montador:
                LogEntry.objects.log_action(
                    user_id         = request.user.pk,
                    content_type_id = ContentType.objects.get_for_model(obj).pk,
                    object_id       = obj.pk,
                    object_repr     = str(obj),
                    action_flag     = CHANGE,
                    change_message  = f"rubrica_montador mudou de {antigo.rubrica_montador} para {obj.rubrica_montador}",
                )

        # Comita a mudança normalmente
        super().save_model(request, obj, form, change)