from django.urls import path
from . import views

urlpatterns = [
    path('registers',views.register, name='urlregister'), 
    path('',views.connexion, name='connexion'),
    path('index',views.index, name='index'),
    path('logout', views.deconnexion, name='urllogout'),
    path('preinscription', views.preinscriptions_view, name='preinscription'),
    path('filiere', views.filieres_view, name='filiere'),
    path('niveau', views.niveaux_view, name='niveau'),
    path('etudiant', views.etudiants_view, name='etudiant'),
    path('matiere', views.matieres_view, name='matiere'),
    path('enseignement', views.enseignements_view, name='enseignement'),
    path('note', views.notes_view, name='note'),
    path('valider-preinscription/<int:preinscription_id>/', views.valider_preinscription, name='valider_preinscription'),
    path('moyenne/<str:matricule>/', views.moyenne_etudiant, name='moyenne_etudiant'),
    path('publier-article/', views.publier_article_view, name='publier_article'),
    path('articles/', views.articles_view, name='article'),
    path('recherche-moyenne/', views.rechercher_moyenne, name='recherche_moyenne'),
    path('options/', views.options_view, name='options'),
    path('emargement/', views.emargement_view, name='emargement'),
    path('emargements/liste', views.liste_emargements_view, name='liste_emargements'),
    #routes ajoutes
    path('email',views.email, name='email'),
    path('modifier/<int:pk>/',views.modifier, name='modifier'),
    path('entrer',views.entrer, name='entrer'),
]