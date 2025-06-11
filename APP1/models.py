from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission


# Utilisateur custom pour gérer étudiants, formateurs, parents, admins
class User(AbstractUser):
    ROLES = (
        ('admin', 'Administrateur'),
        ('formateur', 'Formateur'),
        ('etudiant', 'Étudiant'),
        ('parent', 'Parent'),
    )
    role = models.CharField(max_length=20, choices=ROLES)
    code_formateur = models.CharField(max_length=10, unique=True, null=True, blank=True)
    code_parent = models.CharField(max_length=10, unique=True, null=True, blank=True)
    matricule = models.CharField(max_length=30, unique=True, null=True, blank=True)

# Options/Filières et Niveaux
class Filiere(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Niveau(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class Option(models.Model):
    nom = models.CharField(max_length=100)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - {self.filiere.nom}"

class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'etudiant'})
    option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True)
    date_inscription = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user,self.option,self.niveau,self.date_inscription}"


class Preinscription(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=50, default='en attente')  # validée / rejetée...

    def __str__(self):
        # return f"{self.nom,self.email,self.telephone,self.option,self.statut}"
        return f"{self.nom} - {self.email} - {self.telephone} - {self.option.filiere.nom if self.option and self.option.filiere else 'Aucune filière'} - {self.statut}"

# Matières et attribution
class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    coefficient = models.FloatField()
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom,self.coefficient,self.option}"

class Enseignement(models.Model):
    formateur = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'formateur'})
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.formateur,self.matiere}"
        

# Notes et Moyennes
class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    valeur = models.FloatField()

    def __str__(self):
        return f"{self.etudiant,self.matiere,self.valeur}"

    def get_ponderee(self):
        return self.valeur * self.matiere.coefficient

class Emargement(models.Model):
    formateur = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'formateur'})
    date = models.DateField(default=timezone.now)
    heure_cours = models.FloatField()

    def __str__(self):
        return f"{self.formateur,self.date,self.heure_cours}"

# Articles
class Article(models.Model):
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    approuve = models.BooleanField(default=False)  # pour que l’admin valide ou pas
    def __str__(self):
        return f"{self.auteur,self.titre,self.contenu,self.date_publication,self.approuve}"