Catalogue de livres — Bibliothèque du CSC de Limbé

1. Description du projet

Ce projet a été réalisé dans le cadre du Devoir 1 du cours LOG3550. Il consiste à développer une application web permettant de consulter et de gérer un catalogue de livres pour la Bibliothèque du CSC de Limbé.

L’application utilise HTML5, CSS3 et JavaScript natif, sans framework JavaScript ni framework CSS.

Fonctionnalités principales

* Affichage des livres sous forme de cartes.
* Recherche de livres par titre ou par auteur.
* Filtrage par catégorie et par disponibilité.
* Tri des livres par titre ou par année de publication.
* Ajout et suppression de livres.
* Sauvegarde des données dans le localStorage du navigateur.
* Interface adaptative pour les téléphones, les tablettes et les ordinateurs.

2. Technologies et structure du projet

    2.1. Technologies utilisées

* HTML5 pour structurer le contenu.
* CSS3 pour la mise en forme et le design responsive.
* JavaScript natif pour la recherche, le filtrage et la gestion des livres.
* Git et GitHub pour le suivi des versions et l’hébergement du code source.

    2.2 Structure finale des fichiers

devoir1/
├── index.html
├── css/
│   └── styles.css
├── js/
│   ├── data.js
│   └── app.js
└── README.md

3. Mode d’emploi

a. Ouvrir le fichier index.html dans un navigateur récent.
b. Consulter les livres affichés dans le catalogue.
c. Saisir un titre ou un nom d’auteur dans le champ de recherche.
d. Choisir une catégorie ou utiliser le filtre pour afficher uniquement les livres disponibles.
e. Utiliser le menu de tri pour organiser les livres par titre ou par année.
f. Remplir le formulaire pour ajouter un livre en respectant les règles de validation.
g. Cliquer sur le bouton de suppression pour retirer un livre après confirmation.

Les livres ajoutés ou supprimés sont enregistrés dans le localStorage du navigateur. Les données restent donc disponibles dans le même navigateur après le rechargement de la page.

4. Choix de conception

J’ai choisi HTML5, CSS3 et JavaScript natif afin de respecter les consignes du devoir et de mieux comprendre les bases du développement frontend.

Les balises HTML sémantiques permettent d’organiser clairement le contenu. Le CSS utilise une approche responsive pour adapter la présentation aux différentes tailles d’écran.

Le JavaScript est organisé en fonctions afin de séparer le chargement des données, l’affichage, la recherche, le filtrage et la validation du formulaire.

Le localStorage permet de conserver les modifications sans avoir besoin d’un serveur ou d’une base de données. Enfin, textContent est utilisé pour afficher les données des livres de manière plus sûre.

5. Difficultés rencontrées

L’une des principales difficultés a été d’adapter la grille du catalogue aux différentes tailles d’écran : une colonne sur téléphone, deux sur tablette et trois ou plus sur ordinateur.

La mise en place de la recherche, des filtres et du tri a également demandé une attention particulière afin que les fonctionnalités puissent fonctionner ensemble.

La validation du formulaire a nécessité des contrôles sur le titre, l’auteur, l’année de publication et la catégorie.

Enfin, les tests dans le navigateur et la validation du HTML ont permis de vérifier le fonctionnement et la conformité du projet.

6. Sources et outils d’assistance utilisés

   6.1. Sources

* Documentation MDN Web Docs : https://developer.mozilla.org/
* Validateur HTML du W3C : https://validator.w3.org/

   6.2. Outils d’assistance

* ChatGPT (OpenAI) : utilisé comme outil d’assistance pour comprendre certaines notions, résoudre des difficultés de programmation et améliorer la documentation du projet.
* Navigateur web : utilisé pour tester les fonctionnalités et vérifier l’affichage responsive.
* Git et GitHub : utilisés pour le suivi des modifications et la gestion du dépôt du projet.
* Terminal macOS : utilisé pour créer, modifier, tester et versionner les fichiers du projet.

7. Réponses aux questions théoriques

Question 1 — Pourquoi les balises sémantiques sont-elles préférables à une suite de div ?

Les balises sémantiques comme <header>, <nav>, <main> et <footer> donnent un sens précis au contenu d’une page HTML.
Elles améliorent l’accessibilité en facilitant la navigation des personnes qui utilisent des lecteurs d’écran.
Elles aident les moteurs de recherche à mieux comprendre la structure et le contenu du site.
Elles rendent le code plus clair et plus facile à lire pour les développeurs.
Elles facilitent donc la maintenance du projet, contrairement à une utilisation excessive de div sans signification particulière.

Question 2 — Quelle est la différence entre map, filter et forEach, et lesquels avez-vous utilisés pour la recherche et le filtrage ?

La méthode map() transforme chaque élément d’un tableau et retourne un nouveau tableau contenant les résultats.
La méthode filter() sélectionne les éléments qui respectent une condition et retourne un nouveau tableau.
La méthode forEach() parcourt les éléments d’un tableau sans créer directement un nouveau tableau.
Dans mon projet, j’ai utilisé filter() pour rechercher les livres par titre ou auteur, filtrer par catégorie et afficher uniquement les livres disponibles.
J’ai également utilisé forEach() pour parcourir les livres et les catégories, notamment pour générer les éléments de l’interface.

8. Dépôt GitHub

Le code source du projet est disponible sur GitHub : https://github.com/agrotheo12-collab/LOG3550_D1_Destama_Theonel.git
