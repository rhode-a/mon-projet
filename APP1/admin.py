from django.contrib import admin
from django.contrib import admin
from django.contrib.auth import get_user_model 
User=get_user_model()
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'matricule', 'code_formateur')
    list_filter = ('role',)

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'niveau', 'date_inscription')
    search_fields = ('user__username', 'user__matricule')

@admin.register(Preinscription)
class PreinscriptionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'option','niveau', 'statut')
    list_filter = ('statut',)

class InscriptionAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj =None):
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj =None):
        return request.user.is_staff
    
    def has_add_permission(self, request):
        return request.user.is_staff

@admin.register(Filiere)
@admin.register(Niveau)
@admin.register(Option)
@admin.register(Matiere)
@admin.register(Enseignement)
@admin.register(Note)
@admin.register(Emargement)
@admin.register(Article)
class DefaultAdmin(admin.ModelAdmin):
    pass

