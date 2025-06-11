from django import forms
from django.contrib.auth import get_user_model 
User=get_user_model()
from .models import Article, Emargement,Preinscription

class RechercheMatriculeForm(forms.Form):
    matricule = forms.CharField(
        label='Numéro de matricule',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Ex: TTG-2025-ABCD'})
    )
class ArticleForm(forms.Form):
     class Meta:
        model = Article
        fields = ['auteur', 'titre','contenu','approuve']

class EmargementForm(forms.Form):
    class Meta:
        model = Emargement
        fields = ['formateur','date','heure_cours',]

class PreinscriptionForm(forms.Form):
    class Meta:
        model = Preinscription
        fields = ['nom', 'email', 'telephone','filiere_souhaitee']