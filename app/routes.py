from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from app.models.models import Utilisateur, Etablissement, Categorie, Avis, Possede
from flask_login import login_user, logout_user, login_required, current_user


main = Blueprint('main', __name__)

@main.context_processor
def inject_user():
    return dict(current_user=current_user)
# --- ETABLISSEMENTS ---

# Page d'accueil affichant la carte avec tous les établissements
@main.route("/")
def home():
    etablissements = Etablissement.get_all_json()
    categories = Categorie.get_all_json_raw()
    return render_template("public/menu.html", etablissements=etablissements, categories=categories)

# --- Menu public ---
@main.route('/public/menu')
def menu_public():
    categories = Categorie.get_all_json_raw()
    return render_template('public/menu.html', categories=categories)

# --- Menu admin ---
@main.route('/menu')
@login_required
def menu():
    if not current_user.admin:
        flash("Accès refusé", "error")
        return redirect(url_for('main.menu_public'))
    return render_template('admin/menu.html')

# Blueprint auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.context_processor
def inject_user():
    return dict(current_user=current_user)

@auth.route('/login')
def login():
    return render_template('auth/login.html')


# Récupère tous les établissements (format JSON si besoin)
#@main.route("/etablissements", methods=["GET"])
#def get_etablissements():
#    return jsonify(Etablissement.get_all_json())

@main.route('/etablissements')
def afficher_etablissements():
    etablissements = Etablissement.get_all_json_raw()
    return render_template('admin/etablissements.html', etablissements=etablissements)


# Récupère un établissement par son identifiant (format JSON)
@main.route("/etablissement/<idetab>", methods=["GET"])
def get_etablissement(idetab):
    return jsonify(Etablissement.get_by_id_json(idetab))

# ----------- CREATE -----------

# Formulaire HTML pour ajouter un établissement
@main.route("/etablissement/ajouter", methods=["GET"])
def etablissement_ajouter_form():
    categories = Categorie.get_all_json_raw()
    return render_template("public/ajouter_etablissement.html", categories=categories)

# Traitement POST du formulaire d’ajout
@main.route("/etablissement/ajouter", methods=["POST"])
def ajouter_etablissement():
    data = request.form
    Etablissement.create_from_json(data)
    return redirect(url_for("main.afficher_etablissements"))

# ----------- UPDATE -----------

# Formulaire HTML de modification
@main.route("/etablissement/modifier/<idetab>", methods=["GET"])
def modifier_etablissement_form(idetab):
    etab = Etablissement.query.get_or_404(idetab)
    categories = Categorie.query.all()
    return render_template("public/modifier_etablissement.html", etab=etab, categories=categories)

# Traitement POST du formulaire de modification
@main.route("/etablissement/modifier/<idetab>", methods=["POST"])
def modifier_etablissement(idetab):
    data = request.form
    Etablissement.update_from_json(idetab, data)
    return redirect(url_for("main.home"))

# ----------- DELETE -----------

# Formulaire HTML de confirmation de suppression
@main.route("/etablissement/supprimer/<idetab>", methods=["GET"])
def supprimer_etablissement_form(idetab):
    etab = Etablissement.query.get_or_404(idetab)
    return render_template("public/supprimer_etablissement.html", etab=etab)

# Traitement POST de la suppression (form HTML natif)
@main.route("/etablissement/supprimer/<idetab>", methods=["POST"])
def supprimer_etablissement(idetab):
    Etablissement.delete_by_id(idetab)
    return redirect(url_for("main.home"))

#Route pour barre de recherche
@main.route('/api/etablissements/search')
def search_etablissements():
    q = request.args.get('q', '').strip()
    results = Etablissement.search_by_name(q)
    return jsonify(results)
#Pour gérer l'affichache après dans map
@main.route('/api/etablissements')
def api_etablissements():
    return jsonify(Etablissement.get_all_json())  # ou get_all_json_raw() si c'est mieux

@main.route('/api/etablissements/filter')
def filter_etablissements():
    # On récupère la liste des catégories (peut être plusieurs)
    categories = request.args.getlist('category')
    if not categories:
        return jsonify([])
    # On récupère les établissements filtrés
    etablissements = Etablissement.get_by_categories(categories)
    return jsonify(etablissements)


# --- UTILISATEURS ---

# Affiche la liste de tous les utilisateurs
#@main.route("/utilisateurs", methods=["GET"])
#def get_utilisateurs():
#    return jsonify(Utilisateur.get_all_json())

# Affiche la liste de tous les utilisateurs
@main.route("/utilisateurs", methods=["GET"])
def get_utilisateurs():
    utilisateurs = Utilisateur.get_all_json_raw()
    return render_template("admin/utilisateurs.html", utilisateurs=utilisateurs)             

# Affiche un utilisateur spécifique par son identifiant
@main.route("/utilisateur/<iduser>", methods=["GET"])
def get_utilisateur(iduser):
    return jsonify(Utilisateur.get_by_id_json(iduser))

# Affiche le formulaire pour ajouter un nouvel utilisateur
@main.route("/utilisateur/ajouter", methods=["GET"])
def utilisateur_ajouter_form():
    return render_template("public/ajouter_utilisateur.html")

# Traite le formulaire pour ajouter un nouvel utilisateur                              FAUT RENVOYER SUR UNE PAGE D'AUTHENTIFICATION
@main.route("/utilisateur/ajouter", methods=["POST"])
def ajouter_utilisateur():
    data = request.form
    return jsonify(Utilisateur.create_from_json(data)), 201

# Affiche le formulaire pour modifier un utilisateur existant
@main.route("/utilisateur/modifier/<iduser>", methods=["GET"])
def utilisateur_modifier_form(iduser):
    utilisateur = Utilisateur.get_by_id_json(iduser)
    return render_template("public/modifier_utilisateur.html", utilisateur=utilisateur)

# Traite le formulaire pour modifier un utilisateur                                    FAUT RENVOYER SUR UNE PAGE map
@main.route("/utilisateur/modifier/<iduser>", methods=["POST"])                       
def modifier_utilisateur(iduser):
    data = request.form
    return jsonify(Utilisateur.update_from_json(iduser, data))

# Affiche la page de confirmation pour supprimer un utilisateur                        FAUT RENVOYER SUR UNE PAGE
@main.route("/utilisateur/supprimer/<iduser>", methods=["GET"])                         
def utilisateur_supprimer_form(iduser):
    utilisateur = Utilisateur.get_by_id_json(iduser)
    return render_template("public/supprimer_utilisateur.html", utilisateur=utilisateur)

# Traite la suppression d'un utilisateur
@main.route("/utilisateur/supprimer/<iduser>", methods=["POST"])
def supprimer_utilisateur(iduser):
    return jsonify(Utilisateur.delete_by_id(iduser))


@main.route('/login', methods=['GET'])
def login_form():
    return render_template('auth/login.html')

@main.route('/login', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Utilisateur.authenticate(username, password)
    if user:
        login_user(user)
        if user.admin:
            return redirect(url_for('main.menu'))
        else:
            return redirect(url_for('main.menu_public'))
    else:
        error = "Identifiants invalides"
        return render_template('auth/login.html', error=error)

@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Supprime toutes les données de session
    flash("Déconnexion réussie.", "info")
    return redirect(url_for('main.menu_public'))  # Redirige vers la page de login

@auth.route('/register', methods=['GET'])
def register():
    return render_template('auth/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    data = request.form.to_dict()

    # Vérifications pour username et email déjà pris
    if Utilisateur.query.filter_by(username=data.get('username')).first():
        flash("Nom d'utilisateur déjà pris.", "error")
        return render_template('auth/register.html')

    if Utilisateur.query.filter_by(emailuser=data.get('emailuser')).first():
        flash("Email déjà utilisé.", "error")
        return render_template('auth/register.html')

    # Création utilisateur
    Utilisateur.create_from_json(data)
    flash("Inscription réussie, veuillez vous connecter.", "success")
    return redirect(url_for('auth.login'))


# --- CATEGORIES ---

# Affiche la liste de toutes les catégories (format JSON)
#@main.route("/categories", methods=["GET"])
#def get_categories():
#    return jsonify(Categorie.get_all_json())

@main.route("/categories", methods=["GET"])
def get_categories():
    categories = Categorie.get_all_json_raw()
    return render_template("admin/categorie.html", categorie=categories)     

# Affiche une catégorie spécifique par son identifiant (format JSON)
@main.route("/categorie/<idcat>", methods=["GET"])
def get_categorie(idcat):
    return jsonify(Categorie.get_by_id_json(idcat))

# Affiche le formulaire pour ajouter une nouvelle catégorie
@main.route("/categorie/ajouter", methods=["GET"])
def categorie_ajouter_form():
    return render_template("public/ajouter_categorie.html")

# Traite le formulaire pour ajouter une nouvelle catégorie
@main.route("/categorie/ajouter", methods=["POST"])
def ajouter_categorie():
    data = request.form
    return jsonify(Categorie.create_from_json(data)), 201

# Affiche le formulaire pour modifier une catégorie existante
@main.route("/categorie/modifier/<idcat>", methods=["GET"])
def categorie_modifier_form(idcat):
    categorie = Categorie.get_by_id_json(idcat)
    return render_template("public/modifier_categorie.html", categorie=categorie)

# Traite le formulaire pour modifier une catégorie                                                  FAUT RENVOYER SUR UNE PAGE                       
@main.route("/categorie/modifier/<idcat>", methods=["POST"])
def modifier_categorie(idcat):
    data = request.form
    return jsonify(Categorie.update_from_json(idcat, data))

# Affiche la page de confirmation pour supprimer une catégorie
@main.route("/categorie/supprimer/<idcat>", methods=["GET"])
def categorie_supprimer_form(idcat):
    categorie = Categorie.get_by_id_json(idcat)
    return render_template("public/supprimer_categorie.html", categorie=categorie)

# Traite la suppression d'une catégorie                                                            FAUT RENVOYER SUR UNE PAGE 
@main.route("/categorie/supprimer/<idcat>", methods=["POST"])
def supprimer_categorie(idcat):
    return jsonify(Categorie.delete_by_id(idcat))


# --- AVIS ---

@main.route("/avis", methods=["GET"])
def get_avis():
    avis = Avis.get_all_json_raw()
    return render_template("admin/avis.html", avis=avis) 

# Récupère la liste de tous les avis (format JSON)
#@main.route("/avis", methods=["GET"])
#def get_avis():
#    return jsonify(Avis.get_all_json())

# Récupère un avis par son identifiant (format JSON)
@main.route("/avis/<idav>", methods=["GET"])
def get_avis_by_id(idav):
    return jsonify(Avis.get_by_id_json(idav))

# Affiche le formulaire pour ajouter un nouvel avis (méthode GET)
@main.route("/avis/ajouter", methods=["GET"])                                                     #Si avis deja mis user+etab doit suppp ancien avis et que l'user puisse mettre un new
def ajouter_avis_form():
    return render_template('public/ajouter_avis.html')

# Ajoute un nouvel avis à la base de données (méthode POST)
@main.route("/avis/ajouter", methods=["POST"])
def ajouter_avis():
    data = request.form.to_dict()  # on utilise form pour obtenir les données du formulaire
    return jsonify(Avis.create_from_json(data)), 201

# Affiche le formulaire pour modifier un avis (méthode GET)
@main.route("/avis/modifier/<idav>", methods=["GET"])
def modifier_avis_form(idav):
    avis = Avis.get_by_id_json(idav)
    return render_template('public/modifier_avis.html', avis=avis)

# Modifie un avis existant via son identifiant (méthode PUT)
@main.route("/avis/modifier/<idav>", methods=["POST"])
def modifier_avis(idav):
    data = request.form.to_dict()  # on récupère les données du formulaire
    return jsonify(Avis.update_from_json(idav, data))

# Supprime un avis via son identifiant (méthode DELETE)
@main.route("/avis/supprimer/<idav>", methods=["GET"])
def supprimer_avis_form(idav):
    avis = Avis.get_by_id_json(idav)
    return render_template('public/supprimer_avis.html', avis=avis)

@main.route("/avis/supprimer/<idav>", methods=["POST"])
def supprimer_avis(idav):
    return jsonify(Avis.delete_by_id(idav))


# --- POSSEDE ---

# Récupère la liste de toutes les relations Possede (format JSON)
@main.route("/possede", methods=["GET"])
def get_possedes():
    possedes = Possede.get_all_json_raw()
    return render_template("admin/possede.html", possede=possedes)

# Récupère la liste de toutes les relations Possede (format JSON)
#@main.route("/possede", methods=["GET"])
#def get_possedes():
#    return jsonify(Possede.get_all_json())

# Récupère une relation Possede par idcat et idetab (format JSON)
@main.route("/possede/<idcat>/<idetab>", methods=["GET"])
def get_possede(idcat, idetab):
    return jsonify(Possede.get_by_id_json(idcat, idetab))

# Affiche le formulaire pour ajouter une nouvelle relation Possede
@main.route("/possede/ajouter", methods=["GET"])
def possede_ajouter_form():
    categories = Categorie.get_all_json()  # Liste des catégories
    etablissements = Etablissement.get_all_json()  # Liste des établissements
    return render_template("public/ajouter_possede.html", categories=categories, etablissements=etablissements)

# Ajoute une nouvelle relation Possede à la base de données
@main.route("/possede/ajouter", methods=["POST"])
def ajouter_possede():
    data = request.form  # Récupère les données du formulaire
    Possede.create_from_json(data)  # Crée la relation Possede
    return redirect(url_for("main.home"))  # Redirige vers la page d'accueil

# Affiche le formulaire de confirmation pour supprimer une relation Possede
@main.route("/possede/supprimer/<idcat>/<idetab>", methods=["GET"])
def possede_supprimer_form(idcat, idetab):
    possede = Possede.get_by_id_json(idcat, idetab)  # Récupère la relation à supprimer
    return render_template("public/supprimer_possede.html", possede=possede)

# Supprime une relation Possede via idcat et idetab
@main.route("/possede/supprimer/<idcat>/<idetab>", methods=["POST"])
def supprimer_possede(idcat, idetab):
    Possede.delete_by_id(idcat, idetab)  # Supprime la relation
    return redirect(url_for("main.home"))  # Redirige vers la page d'accueil

# Supprime une relation Possede via idcat et idetab (format JSON)
@main.route("/possede/supprimer/<idcat>/<idetab>", methods=["DELETE"])
def supprimer_possede_json(idcat, idetab):
    return jsonify(Possede.delete_by_id(idcat, idetab))

# Affiche le formulaire pour modifier une relation Possede
@main.route("/possede/modifier/<idcat>/<idetab>", methods=["GET"])
def possede_modifier_form(idcat, idetab):
    possede = Possede.get_by_id_json(idcat, idetab)  # Récupère la relation à modifier
    categories = Categorie.get_all_json()  # Liste des catégories
    etablissements = Etablissement.get_all_json()  # Liste des établissements
    return render_template("public/modifier_possede.html", possede=possede, categories=categories, etablissements=etablissements)

# Modifie une relation Possede existante
@main.route("/possede/modifier/<idcat>/<idetab>", methods=["POST"])
def modifier_possede(idcat, idetab):
    data = request.form  # Récupère les données du formulaire
    possede = Possede.query.get_or_404((idcat, idetab))  # Récupère la relation existante
    Possede.update_from_form(possede, data)  # Met à jour la relation
    return redirect(url_for("main.home"))  # Redirige vers la page d'accueil
