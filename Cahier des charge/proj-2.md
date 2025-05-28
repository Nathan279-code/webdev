### Projet

Web app


## Le site en question
# Site - Publique
Repertorie etablissement (addr)

Users (page de co, etc.)

Pub. - No login
User, si pas co pt voir la map a x km et voir les icones
les icones sont des types detablissements
filtrer via categorie detablissement
Barre de recherche (nom etablissement)

Pub. - User login 
Attribue une note (Bonus: commentaire) a un etablissement
Moyenne des notes a afficher lorsque on clique sur un etablissement

# Site - Prive
BD - BackOffice (python)
Pour les admins des sites
Ajouter, supp, modif etablissement


## La Map et localisation
Google API 
    pb: Necessaire CB meme si gratos
    => un fdp pourrait forcer les req et donc nous faire payer
Leaflet :
    bibli js qui utilse OpenStreetMap
    suggestion du prof

Centrer sur notre position

Longitude, lattitude (pour placer les icones)
    Comment les obtenir avec une addr
    Geolocalisation API Google
        -> Alternative: OpenStreetMap as aussi une geolocalisation


## Contraintes
Modele MVC Obligatoire (Modele, vue, controlleur)
    Model: Modelisation de nos objets
    View: Partie affichage de l'app
    Controller: Moteur de l'app (Tout le reste)

html/css/js
Python web - Flask

Partie publique(affichage) doit marcher pour mobile (responsive design)

Utiliser github

## Cahier des charges
Cahier des charge 1-2pages
    Fonctionelle et technique
    Explique but du projet et architecture
    Quelle BD et a quoi elle ressemble et, son modele, schema BD
        UML
        DB Diagramme recommende (pt prendre SQL)
    Langauges et outils
    Barrieres du projet (de facon global, pas besoin de tout dire)


## Permissions
Tempalte css tout pret autorise (bootstrap)
    Conseil: Different pour BackOffice et Publique
    On seras pas note sur la beaute


## Normes de codage
W3C (bonus aucun warning)
    Indulgent sur BackOffice
    Mais stricte sur Publique

Facilement maintenable
    Gros bloques doivent etre commente
    Ainsi que des noms bien adaptes


## Poo & CRUD
CRUD des objets:
Create
Read
Update
Delete

- Objets qui doivent pouvoir CRUD
    - Utilisateurs
    - Etablissements
    - Categories d'etablissements
    - (Un autre, a nous de voir plus tard...)

Noter sur la facon de gerer CRUD


## Attention
Si on peut add commentaire sans connecter - pb
Si on peut acceder au BackOffice sans connecter - gros pb


# Autres recommendations
Commencer par cahier des charges
Tester leaflet et ses cartes