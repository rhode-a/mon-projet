from django.shortcuts import render, get_object_or_404, redirect
from .models import Preinscription, User, Etudiant, Option, Niveau, Note, Article, Emargement,Filiere,Matiere,Enseignement
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import RechercheMatriculeForm, ArticleForm, EmargementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model 
User=get_user_model()

@login_required
def valider_preinscription(request, preinscription_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Vous n'avez pas la permission de valider une inscription.")

    preins = get_object_or_404(Preinscription, id=preinscription_id)

    # Si déjà validée => on évite une nouvelle création
    if preins.statut == 'validée':
        messages.info(request, f"La préinscription de {preins.nom} a déjà été validée.")
        return redirect('preinscription')

    # Vérifier si un utilisateur avec ce mail existe déjà
    if User.objects.filter(username=preins.email).exists():
        messages.warning(request, f"Un utilisateur avec cet email existe déjà.")
        return redirect('preinscription')

    # Création du compte utilisateur
    user = User.objects.create_user(
        username=preins.email,  # ou une construction unique
        email=preins.email,
        role='etudiant',
        first_name=preins.nom,
    )

    # Création de l'étudiant
    Etudiant.objects.create(
        user=user,
        option=preins.option,
        niveau=preins.niveau
    )

    # Mise à jour du statut
    preins.statut = 'validée'
    preins.save()

    # Envoi de l'email
    try:
        send_mail(
            'Confirmation de votre inscription - TTG Network',
            f'Bonjour {preins.nom}, votre inscription a été validée. Identifiant : {user.matricule}.',
            'ttg@example.com',
            [preins.email],
            fail_silently=False
        )
    except Exception as e:
        messages.warning(request, f"Utilisateur créé, mais l'email n'a pas pu être envoyé : {e}")

    messages.success(request, f"Préinscription validée avec succès pour {preins.nom}.")
    return redirect('etudiant')


@login_required
def moyenne_etudiant(request, matricule):
    etudiant = get_object_or_404(Etudiant, user__matricule=matricule)
    notes = Note.objects.filter(etudiant=etudiant)

    if not notes.exists():
        return render(request, 'moyenne.html', {'etudiant': etudiant, 'message': "Aucune note trouvée."})

    total_pondere = 0
    total_coefficients = 0
    notes_detail = []

    for note in notes:
        coeff = note.matiere.coefficient
        ponderee = note.valeur * coeff
        total_pondere += ponderee
        total_coefficients += coeff
        notes_detail.append({
            'matiere': note.matiere.nom,
            'valeur': note.valeur,
            'coefficient': coeff,
            'ponderee': ponderee
        })

    moyenne = total_pondere / total_coefficients if total_coefficients > 0 else 0

    return render(request, 'moyenne.html', {
        'etudiant': etudiant,
        'notes': notes_detail,
        'moyenne': round(moyenne, 2)
    })

@login_required
def rechercher_moyenne(request):
    moyenne = None
    mention = None
    matricule = None

    if request.method == 'POST':
        form = RechercheMatriculeForm(request.POST)
        if form.is_valid():
            matricule = form.cleaned_data['matricule']
            try:
                etudiant = Etudiant.objects.get(user__matricule=matricule)
                notes = Note.objects.filter(etudiant=etudiant)

                total_points = sum([n.get_ponderee() for n in notes])
                total_coeff = sum([n.matiere.coefficient for n in notes])

                moyenne = total_points / total_coeff if total_coeff > 0 else 0

                # Déterminer la mention
                if moyenne >= 16:
                    mention = "Très bien"
                elif moyenne >= 14:
                    mention = "Bien"
                elif moyenne >= 12:
                    mention = "Assez bien"
                elif moyenne >= 10:
                    mention = "Passable"
                else:
                    mention = "Insuffisant"

            except Etudiant.DoesNotExist:
                form.add_error('matricule', 'Étudiant introuvable.')
    else:
        form = RechercheMatriculeForm()

    return render(request, 'recherche_moyenne.html', {
        'form': form,
        'moyenne': moyenne,
        'mention': mention,
        'matricule': matricule
    })


@login_required
def options_view(request):
    options = Option.objects.all()
    return render(request, 'options.html', {'options': options})

@login_required
def preinscriptions_view(request):
    preinscriptions = Preinscription.objects.all()
    return render(request, 'liste_preinscriptions.html', {'preinscriptions': preinscriptions})

@login_required
def filieres_view(request):
    filieres = Filiere.objects.all()
    return render(request, 'liste_filieres.html', {'filieres': filieres})

@login_required
def niveaux_view(request):
    niveaux = Niveau.objects.all()
    return render(request, 'liste_niveaux.html', {'niveaux': niveaux})

@login_required
def etudiants_view(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'liste_etudiants.html', {'etudiants': etudiants})

@login_required
def matieres_view(request):
    matieres = Matiere.objects.all()
    return render(request, 'liste_matieres.html', {'matieres': matieres})

@login_required
def enseignements_view(request):
    enseignements = Enseignement.objects.all()
    return render(request, 'liste_enseignements.html', {'enseignements': enseignements})


@login_required
def notes_view(request):
    notes = Note.objects.all()
    return render(request, 'liste_notes.html', {'notes': notes})


@login_required
def articles_view(request):
    articles = Article.objects.all()
    return render(request, 'liste_articles.html', {'articles': articles})

@login_required
def publier_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.save()
            return redirect('liste_articles')
    else:
        form = ArticleForm()
    return render(request, 'publier_article.html', {'form': form})

@login_required
def emargement_view(request):
    if request.method == 'POST':
        form = EmargementForm(request.POST)
        if form.is_valid():
            emargement = form.save(commit=False)
            emargement.formateur = request.user
            emargement.save()
            return redirect('liste_emargements')
    else:
        form = EmargementForm()
    return render(request, 'emargement.html', {'form': form})

@login_required
def liste_emargements_view(request):
    emargements = Emargement.objects.all()
    return render(request, 'liste_emargements.html', {'emargements': emargements})


#L'authentification
def register(request): 
    if not request.user.is_staff:
        return HttpResponseForbidden("vous n'avez pas la permission de valider une inscription")
    if request.method == 'POST': 
        nom = request.POST.get('nom') 
        email = request.POST.get('email') 
        password1 = request.POST.get('password1') 
        password2 = request.POST.get('password2') 
        role=request.POST.get('role')
        if password1 != password2: 
            messages.error(request, "Les mots de passe ne correspondent pas.") 
            print("les deux mots de passes ne sont pas identiques*") 
            return render(request, 'register.html') 
        else: 
            print("les deux mots de passes sont identiques") 
            if len(password1) < 8: 
                messages.error(request, "Le mot de passe doit avoir au moins 8 caractères.") 
                print("la taille du mot de passe est inferieur à 8 caractères") 
                return render(request, 'register.html') 
            else: 
                print("la taille du mot de passe est valide") 
                if User.objects.filter(username=nom).exists(): 
                    messages.error(request, "Un utilisateur avec ce nom existe déjà") 
                    print("cet utilisateur existe déjà ") 
                    return render(request, 'register.html') 
                else: 
                    print("cet utilisateur n'existe pas") 
                    user = User.objects.create_user(username=nom, email=email, password=password1, role=role ) 
                    messages.success(request, "Compte créé avec succès! Vous pouvez maintenant vous connecter.") 
                    print('compte creer ') 
                    return redirect('connexion') 
    return render(request, 'register.html')

#la connexion
def connexion(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        password = request.POST.get('password')

        user = None

        # Cas 1 : identifiant classique (admin/parent)
        user = authenticate(request, username=nom, password=password)
        if user:
            login(request, user)
            return redirect('index')

        # Cas 2 : connexion via matricule (étudiant)
        try:
            user = User.objects.get(matricule=password)
            login(request, user)
            return redirect('index')
        except User.DoesNotExist:
            pass
        
         # Cas 3 : connexion via Code parent (Parent)
        try:
            user = User.objects.get(code_parent=password)
            login(request, user)
            return redirect('index')
        except User.DoesNotExist:
            pass

        # Cas 4 : connexion via code formateur
        try:
            user = User.objects.get(code_formateur=password)
            login(request, user)
            return redirect('index')
        except User.DoesNotExist:
            pass

        messages.error(request, "Identifiant ou mot de passe invalide.")

    return render(request, 'login.html')



@login_required 
def index(request): 
    return render(request, 'index.html') 

@login_required 
def deconnexion(request): 
    logout(request) 
    return redirect('urllogout')


#les nouvelles vues
def email(request): 
    if request.method == "POST":
        data=request.POST
        email=data.get("email")
        user=User.objects.filter(email=email).last()
        if user:
            print("l'email est bien correct")
            return redirect("modifier", user.id)
        else:
            print("l'email est incorrect")
            return redirect("email")
    return render(request, 'email.html') 

def modifier(request,pk): 
    if request.method == "POST":
        data=request.POST
        if data.get("password")==data.get("confirm_password"):
            user=User.objects.get(id=int(pk))
            user.set_password(data.get("password"))
            user.save()
            return redirect("connexion")
        else:
            return redirect("modifier",user.id)   
    return render(request, 'modifier.html')

def entrer(request): 
    if request.method == 'POST': 
        nom = request.POST.get('nom') 
        email = request.POST.get('email') 
        password1 = request.POST.get('password1') 
        password2 = request.POST.get('password2') 
        role=request.POST.get('role')
        if password1 != password2: 
            messages.error(request, "Les mots de passe ne correspondent pas.") 
            print("les deux mots de passes ne sont pas identiques*") 
            return render(request, 'entrer.html') 
        else: 
            print("les deux mots de passes sont identiques") 
            if len(password1) < 8: 
                messages.error(request, "Le mot de passe doit avoir au moins 8 caractères.") 
                print("la taille du mot de passe est inferieur à 8 caractères") 
                return render(request, 'entrer.html') 
            else: 
                print("la taille du mot de passe est valide") 
                if User.objects.filter(username=nom).exists(): 
                    messages.error(request, "Un utilisateur avec ce nom existe déjà") 
                    print("cet utilisateur existe déjà ") 
                    return render(request, 'entrer.html') 
                else: 
                    print("cet utilisateur n'existe pas") 
                    user = User.objects.create_user(username=nom, email=email, password=password1, role=role ) 
                    messages.success(request, "Compte créé avec succès! Vous pouvez maintenant vous connecter.") 
                    print('compte creer ') 
                    return redirect('connexion') 
    return render(request,'entrer.html')