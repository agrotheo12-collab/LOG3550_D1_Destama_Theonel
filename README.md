# API Bibliothèque — Catalogue de livres du Collège Sainte Croix de Limbé

## 1. Présentation du projet

Ce projet a été réalisé dans le cadre du **Devoir 2 du cours LOG3550**. Il constitue la deuxième étape du développement d'un catalogue numérique de livres pour la bibliothèque du Collège Sainte Croix de Limbé.

L'objectif est de transformer le catalogue initial en une application client-serveur. Le backend expose une API REST développée avec FastAPI, tandis que le frontend communique avec cette API pour consulter, ajouter et supprimer des livres.

Les données sont enregistrées dans une base de données SQLite.

## 2. Technologies utilisées

### Backend
- Python 3.14
- FastAPI : création de l'API REST
- Uvicorn : serveur ASGI
- SQLModel : gestion des modèles et interactions avec la base de données
- SQLite : système de gestion de base de données
- Pydantic : validation des données
- Pytest et HTTPX : tests automatisés de l'API

### Frontend
- HTML5
- CSS3
- JavaScript
- Fetch API : communication avec le backend

### Outils
- Visual Studio Code
- Terminal macOS
- Git et GitHub
- Swagger UI : documentation et tests interactifs de l'API

## 3. Structure du projet

```text
LOG3550_D2_Projet/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── livres.py
│   │
│   ├── tests/
│   │   └── test_livres.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── data.js
│       └── app.js
│
├── .gitignore
└── README.md
```

La base de données `bibliotheque.db` est créée automatiquement au démarrage de l'API. L'environnement virtuel `.venv` est utilisé pour le développement et n'est pas destiné à être remis avec le projet.

## 4. Installation et configuration

### 4.1. Prérequis

- Python 3.10 ou une version supérieure
- pip
- Un navigateur Web
- Git

### 4.2. Accéder au backend

Depuis le répertoire principal du projet :

```bash
cd backend
```

### 4.3. Créer l'environnement virtuel

```bash
python3 -m venv .venv
```

### 4.4. Activer l'environnement virtuel

Sur macOS ou Linux :

```bash
source .venv/bin/activate
```

### 4.5. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 5. Démarrage de l'application

### 5.1. Lancer le backend

Dans un terminal, depuis le dossier `backend`, avec l'environnement virtuel activé :

```bash
python -m uvicorn app.main:app --reload
```

L'API est accessible à l'adresse :

http://127.0.0.1:8000

### 5.2. Accéder à la documentation Swagger

La documentation interactive est disponible à l'adresse :

http://127.0.0.1:8000/docs

Elle permet de consulter les routes, leurs descriptions, les modèles de données et des exemples JSON pour les opérations de création et de modification.

### 5.3. Lancer le frontend

Ouvrir un deuxième terminal et exécuter :

```bash
cd frontend
python3 -m http.server 5500
```

Ouvrir ensuite le navigateur à l'adresse :

http://127.0.0.1:5500

Le frontend communique avec le backend à l'aide de requêtes HTTP. Le serveur backend doit donc être démarré pour que le catalogue puisse fonctionner correctement.

## 6. Fonctionnalités de l'application

L'application permet de :

- Consulter la liste des livres.
- Rechercher un livre par son titre ou le nom de son auteur.
- Filtrer les livres par catégorie.
- Filtrer les livres selon leur disponibilité.
- Trier les résultats.
- Ajouter un nouveau livre.
- Supprimer un livre.
- Afficher les messages de chargement et les erreurs de connexion à l'API.

Les opérations de consultation, d'ajout et de suppression du frontend sont effectuées à travers l'API avec JavaScript et Fetch API. Les données ne sont plus enregistrées dans `localStorage`.

## 7. Modèle de données et validation

Chaque livre possède les champs suivants :

| Champ | Description |
|---|---|
| id | Identifiant généré automatiquement |
| titre | Titre du livre |
| auteur | Auteur du livre |
| annee | Année de publication |
| categorie | Catégorie du livre |
| isbn | ISBN facultatif et unique |
| disponible | Disponibilité du livre |

### Règles de validation

- Le titre doit contenir entre 2 et 200 caractères.
- Le nom de l'auteur doit contenir entre 2 et 200 caractères.
- L'année doit être comprise entre 1450 et l'année actuelle.
- La catégorie doit appartenir aux catégories autorisées.
- L'ISBN, lorsqu'il est fourni, doit contenir exactement 10 ou 13 chiffres.
- La disponibilité est définie à `true` par défaut.
- L'identifiant est généré par la base de données et ne doit pas être fourni par le client.

### Catégories disponibles

- Roman
- Science-fiction
- Littérature
- Histoire
- Informatique
- Développement personnel
- Religion
- Langue

## 8. Base de données

Le projet utilise SQLite avec SQLModel pour la gestion des données.

La base de données est créée automatiquement au démarrage de l'application. Lorsqu'elle est vide, dix livres initiaux sont ajoutés automatiquement.

La contrainte d'unicité de l'ISBN est également appliquée au niveau de la base de données afin d'éviter l'enregistrement de deux livres possédant le même ISBN.

Le fichier de la base de données est créé dans le dossier `backend/`.

## 9. Routes de l'API REST

| Méthode HTTP | Route | Description |
|---|---|---|
| GET | `/sante` | Vérifier l'état de l'API |
| GET | `/livres/` | Consulter et filtrer les livres |
| GET | `/livres/{id}` | Consulter un livre par son identifiant |
| POST | `/livres/` | Ajouter un livre |
| PUT | `/livres/{id}` | Remplacer complètement un livre |
| PATCH | `/livres/{id}` | Modifier partiellement un livre |
| DELETE | `/livres/{id}` | Supprimer un livre |

La route de consultation de la liste accepte notamment les paramètres suivants :

- `q` : rechercher dans le titre ou le nom de l'auteur.
- `categorie` : filtrer par catégorie.
- `disponible` : filtrer selon la disponibilité.
- `skip` : définir le nombre de résultats à ignorer.
- `limit` : limiter le nombre de résultats retournés.

L'API utilise notamment les codes HTTP suivants :

- `200` : requête réussie.
- `201` : livre créé.
- `204` : livre supprimé avec succès.
- `404` : livre introuvable.
- `409` : conflit, notamment en cas d'ISBN déjà utilisé.
- `422` : données invalides.

## 10. Tests automatisés

Les tests sont réalisés avec Pytest et le client de test de FastAPI.

Ils utilisent une base de données SQLite temporaire en mémoire afin de ne pas modifier les données de la base utilisée par l'application.

Pour exécuter les tests, ouvrir un terminal dans le dossier `backend`, activer l'environnement virtuel, puis exécuter :

```bash
python -m pytest -v
```

La suite de tests comprend notamment :

- La création d'un livre.
- La consultation d'un livre.
- La consultation avec filtres.
- Le remplacement complet d'un livre.
- La modification partielle d'un livre.
- La suppression d'un livre.
- La gestion d'un livre introuvable.
- La validation des données.
- La validation des catégories et de l'ISBN.
- La détection d'un ISBN en double.
- La vérification de l'état de l'API.
- Le rejet d'un identifiant fourni directement par le client.

**Résultat obtenu lors de la dernière exécution : 12 tests réussis.**

## 11. Configuration CORS

Le middleware CORS est configuré dans le backend afin d'autoriser le frontend servi depuis l'origine suivante :

`http://127.0.0.1:5500`

Cette configuration permet au navigateur de communiquer avec l'API tout en limitant les origines autorisées.

## 12. Explications techniques

### FastAPI, Uvicorn et Pydantic

FastAPI est le framework utilisé pour construire l'API REST et définir les routes HTTP. Uvicorn est le serveur ASGI qui exécute l'application et reçoit les requêtes. Pydantic valide les données reçues et permet de contrôler leur format avant leur traitement.

### Séparation entre modèles et schémas

Le modèle SQLModel représente la structure des données enregistrées dans la base de données. Les schémas Pydantic définissent les données acceptées à l'entrée et celles retournées par l'API. Cette séparation améliore la sécurité et facilite la maintenance du code.

### Différence entre PUT et PATCH

PUT sert à remplacer complètement les données d'une ressource. PATCH sert à modifier seulement certains champs sans remplacer les autres. Une opération idempotente produit le même état final lorsqu'elle est répétée avec les mêmes données. Dans cette application, les modifications PUT et PATCH définissent des valeurs, ce qui permet de conserver le même état final lorsqu'une même modification est répétée.

## 13. Dépôt GitHub

Le code source du projet est disponible sur GitHub :

https://github.com/agrotheo12-collab/LOG3550_D1_Destama_Theonel

La branche utilisée pour le Devoir 2 est `devoir2`.

---

**Cours :** LOG3550  
**Travail :** Devoir 2 — Développement d'une API REST  
**Institution :** Collège Sainte Croix de Limbé
