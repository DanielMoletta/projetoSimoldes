# signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from .middleware import get_current_user
from .models import Processo

@receiver(pre_save, sender=Processo)
def cache_old_rubricas(sender, instance, **kwargs):
    if not instance.pk:
        return
    antigo = sender.objects.get(pk=instance.pk)
    # guarda em atributos temporários do próprio instance
    instance._old_rubrica = antigo.rubrica
    instance._old_rm      = antigo.rubrica_montador

@receiver(post_save, sender=Processo)
def log_rubricas(sender, instance, created, **kwargs):
    if created:
        return
    user = get_current_user()
    if not user or not user.is_authenticated:
        return

    # pega o estado que a gente guardou no pre_save
    old_r  = getattr(instance, '_old_rubrica', None)
    old_rm = getattr(instance, '_old_rm', None)

    msgs = []
    if old_r  is not None and old_r  != instance.rubrica:
        msgs.append(f"rubrica: {old_r} → {instance.rubrica}")
    if old_rm is not None and old_rm != instance.rubrica_montador:
        msgs.append(f"rubrica_montador: {old_rm} → {instance.rubrica_montador}")

    if not msgs:
        return

    LogEntry.objects.log_action(
        user_id         = user.pk,
        content_type_id = ContentType.objects.get_for_model(instance).pk,
        object_id       = instance.pk,
        object_repr     = str(instance),
        action_flag     = CHANGE,
        change_message  = "; ".join(msgs),
    )
