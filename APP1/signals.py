from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from .models import User, Etudiant
from datetime import datetime

@receiver(post_save, sender=User)
def generate_identifiants(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'etudiant' and not instance.matricule:
            annee = datetime.now().year
            instance.matricule = f'TTG-{annee}-{get_random_string(4).upper()}'
            instance.save()
        elif instance.role == 'formateur' and not instance.code_formateur:
            instance.code_formateur = f'FORM-{get_random_string(5).upper()}'
            instance.save()
        elif instance.role == 'parent' and not instance.code_parent:
            instance.code_parent = f'PART-{get_random_string(5).upper()}'
            instance.save()