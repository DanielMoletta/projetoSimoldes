from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from .models import Processo

@receiver(pre_save, sender=Processo)
def cache_old_rubricas(sender, instance, **kwargs):
    if not instance.pk:
        return
    antigo = sender.objects.get(pk=instance.pk)
    instance._old_rubrica = antigo.rubrica
    instance._old_rm      = antigo.rubrica_montador

@receiver(post_save, sender=Processo)
def log_rubricas(sender, instance, created, **kwargs):
    if created:
        return

    old_r  = getattr(instance, '_old_rubrica', None)
    old_rm = getattr(instance, '_old_rm', None)

    msgs = []
    entry_user = None

    # Se mudou a rubrica "normal"
    if old_r is not None and old_r != instance.rubrica:
        u = instance.rubrica_user
        nome = (u.get_full_name() or u.username) if u else '—'
        msgs.append(f"rubrica: {old_r} → {instance.rubrica} (por {nome})")
        entry_user = u

    # Se mudou a rubrica do montador
    if old_rm is not None and old_rm != instance.rubrica_montador:
        u2 = instance.rubrica_montador_user
        nome2 = (u2.get_full_name() or u2.username) if u2 else '—'
        msgs.append(f"rubrica_montador: {old_rm} → {instance.rubrica_montador} (por {nome2})")
        # Se entry_user ainda não foi definido, usamos o montador
        if entry_user is None:
            entry_user = u2

    if not msgs or entry_user is None:
        # sem mudanças relevantes ou sem um user para atribuir, não loga
        return

    LogEntry.objects.log_action(
        user_id         = entry_user.pk,
        content_type_id = ContentType.objects.get_for_model(instance).pk,
        object_id       = instance.pk,
        object_repr     = str(instance),
        action_flag     = CHANGE,
        change_message  = "; ".join(msgs),
    )