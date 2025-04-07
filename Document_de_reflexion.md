
# 🧠 Document de Réflexion – Projet Suivi de Réseau

## 🧭 Introduction

### 📌 Présentation du sujet choisi

Dans le cadre du projet final de gestion de code source, j’ai choisi l’**option B** : le développement d’un outil de **suivi réseau** capable de scanner une plage d’adresses IP. Ce choix s’est imposé naturellement, car il correspond à des problématiques courantes dans le domaine de l'administration système et réseau, notamment la surveillance de la connectivité des équipements, l’identification des machines actives sur un réseau local, et la détection de services exposés via des ports ouverts.

Le projet consiste à concevoir un utilitaire en ligne de commande capable de :
- **scanner une plage d’IP** ou un fichier de configuration personnalisé ;
- **afficher les IP actives ou inactives**, ainsi que leur **latence moyenne** ;
- **sauvegarder les résultats** dans un fichier CSV ;
- **effectuer un scan asynchrone** pour améliorer la vitesse ;
- **détecter les ports ouverts** (TCP) avec `nmap` sur les machines actives.

### 🎯 Objectifs et organisation du projet

L’objectif principal était de transformer un script basique en une application Python **structurée, modulaire, testée et documentée**, respectant les standards professionnels de développement logiciel. Le projet devait aussi mettre en œuvre une **intégration continue**, une **documentation automatisée** et une **couverture de tests rigoureuse**.

L’organisation du projet a suivi une architecture claire :

- **`src/`** : contient le cœur de l'application, découpé en modules `core/` et `utils/`.
- **`tests/`** : inclut les tests unitaires couvrant les différents modules.
- **`docs/`** : contient la documentation Sphinx, structurée avec des fichiers `.rst`.
- **`data/`** : pour stocker les fichiers CSV d'entrée et de résultats.
- **GitHub Actions** : gère les workflows de test, linting et déploiement de la documentation.

Chaque fonctionnalité a été conçue de manière modulaire, testée indépendamment, puis intégrée dans une logique métier unifiée accessible via un unique point d’entrée : `main.py`. L’interface en ligne de commande repose sur `argparse`, permettant une utilisation souple et explicite pour l’utilisateur final.


Voici une vue plus détaillée de l’organisation technique du dépôt :

- **.github/workflows/** : contient les fichiers YAML des workflows GitHub Actions :
  - `tests.yml` : exécute les tests unitaires, la couverture de code, `flake8` et `pylint`.
  - `deploy-doc.yml` : construit et déploie la documentation Sphinx sur GitHub Pages.

- **data/** : contient les fichiers de configuration (`machines.csv`) et les résultats de scan générés automatiquement en fonction du mode choisi (fichier ou plage IP).

- **docs/** : documentation Sphinx complète avec fichiers `.rst`, configuration `conf.py`, et scripts de build (`Makefile`, `make.bat`).

- **src/** : cœur de l’application Python, divisé en deux sous-modules :
  - `core/` : logique réseau (ping, scan de ports, coordination, async/thread).
  - `utils/` : gestion CSV, parsing de latence, logger.

- **tests/** : tests unitaires couvrant tous les modules fonctionnels du projet, avec une très bonne couverture (y compris les cas asynchrones).

- **README.md** et **.gitignore** : fichiers classiques d’accueil de projet et d’exclusion Git.

## 🛠️ Développement

### 🔧 Étapes principales réalisées

1. Création de la structure initiale avec `src/`, `tests/`, `docs/` et `data/`.
2. Développement des modules principaux : `ping`, `runner`, `scanner_threaded`, `scanner_async`, `port_scanner`.
3. Intégration d’un système de log (`logger.py`) et de parsing de la latence réseau (`parsing.py`).
4. Mise en place de la gestion des fichiers CSV en lecture/écriture.
5. Ajout du support `argparse` pour gérer les entrées utilisateur.
6. Implémentation des tests unitaires avec `unittest`, `patch`, `mock`, `AsyncMock`.
7. Configuration de l’intégration continue avec GitHub Actions.
8. Génération de la documentation avec Sphinx.

### 🧱 Problèmes rencontrés et solutions apportées

Globalement, le développement du projet s’est bien déroulé grâce à une architecture claire et à une organisation en modules indépendants. Cependant, quelques défis techniques ont nécessité des ajustements spécifiques :

- **Compatibilité multi-plateforme pour la récupération de la latence réseau**  
  Lors de l’analyse des résultats de commande `ping`, les formats de sortie variaient fortement selon l’OS (Linux, Windows en français, Windows en anglais). Cela entraînait des échecs d’extraction de la latence.  
  ➤ J’ai corrigé cela en élargissant les expressions régulières dans `extract_latency()` pour prendre en charge tous les formats connus, avec un **fallback générique** qui capte des chaînes de type `time=XX ms` au cas où les formats standards échoueraient.

- **Décodage des sorties `ping` en asynchrone**  
  En mode asynchrone (`asyncio.create_subprocess_exec`), j’ai rencontré des problèmes de décodage lorsque la sortie contenait des caractères non UTF-8. Cela générait une `UnicodeDecodeError`.  
  ➤ J’ai mis en place un **système de décodage adaptatif** : tentative initiale en UTF-8, puis fallback en `latin1`, ce qui assure la compatibilité avec les encodages les plus courants.

- **Échec de résolution DNS avec certaines IP**  
  Pour les IP non associées à un nom d’hôte, la fonction `socket.gethostbyaddr` levait une `socket.herror`, ce qui pouvait interrompre l'exécution.  
  ➤ J’ai encapsulé cet appel dans un bloc `try/except` dans `resolve_hostname_if_needed()`, avec **retour de l’IP brute comme fallback** si la résolution échoue.

- **Tests unitaires pour fonctions asynchrones**  
  Tester les fonctions async (notamment `async_ping_ip`) demandait une structure différente du testing classique.  
  ➤ J’ai utilisé `IsolatedAsyncioTestCase` ainsi que `AsyncMock` pour simuler les comportements asynchrones, ce qui a permis de couvrir correctement tous les cas, y compris les erreurs réseau simulées.

- **Disponibilité de Nmap en environnement GitHub Actions**  
  Le scan de ports nécessite `nmap`, qui n’est pas présent par défaut dans les runners GitHub.  
  ➤ J’ai ajouté son installation dans le workflow CI (`sudo apt-get install -y nmap`) pour garantir le bon déroulement des tests en mode `--ports`.


## 🔁 Pipeline CI/CD

Le pipeline CI/CD a été mis en place avec **GitHub Actions** afin de garantir automatiquement la qualité, la stabilité et la maintenabilité du projet à chaque modification du code source. Deux workflows distincts ont été créés et sont situés dans le dossier `.github/workflows/`.

---

### 🧪 `tests.yml` – Tests, couverture et qualité de code

Ce workflow est exécuté à chaque `push` ou `pull request` sur n’importe quelle branche. Il a pour rôle de :

- 🔁 **Tester sur plusieurs versions de Python** : le projet est vérifié sous Python `3.8`, `3.10`, `3.11` et `3.12` pour s’assurer de sa portabilité.
- 📦 **Installer les dépendances** : `nmap`, `pip`, `flake8`, `pylint`, `coverage`, etc.
- ✅ **Analyser le code avec `flake8`** : détecte les violations de la PEP8.
- 📊 **Évaluer la qualité du code avec `pylint`** : avec un score minimum exigé de **9.0/10**. Si ce score n’est pas atteint, le workflow échoue.
- 🧪 **Exécuter les tests unitaires** : via `coverage run`, couvrant tous les modules du répertoire `src/`.
- 📈 **Générer un rapport de couverture HTML** et un rapport console détaillé.
- ☁️ **Uploader les rapports** (`flake8`, `pylint`, `htmlcov/`) comme artefacts téléchargeables dans l’interface GitHub.

Ce pipeline permet de détecter immédiatement les régressions, erreurs de style ou pertes de couverture dès qu’une modification est introduite.

---

### 📘 `deploy-doc.yml` – Documentation automatique

Ce deuxième workflow est exécuté à chaque `push` ou `pull request`. Il s’active plus précisément lorsque la branche `main` reçoit un commit, et il :

- ✅ **Installe les dépendances Sphinx** (`sphinx`, `sphinx_rtd_theme`, `myst_parser`).
- 🧱 **Construit la documentation HTML** à partir des fichiers `.rst` du dossier `docs/source/`.
- 🚀 **Déploie automatiquement la documentation** sur GitHub Pages (branche `gh-pages`) grâce à l’action `peaceiris/actions-gh-pages@v3`.

Cela garantit que la documentation en ligne reste toujours **synchronisée avec le code source**, sans intervention manuelle.

---

### 🧠 Objectif du pipeline

Le pipeline CI/CD mis en place répond aux objectifs suivants :
- **Assurer un niveau de qualité constant** à chaque modification du projet.
- **Automatiser les tâches répétitives** (tests, analyse statique, documentation).
- **Renforcer la confiance** dans les modifications via des validations automatiques.
- **Simplifier le travail de maintenance** et de revue de code, notamment en contexte collaboratif.

---

## ✅ Conclusion et auto-évaluation

### 🔍 Bilan personnel

🟩 Dans l’ensemble, je suis satisfait du travail accompli. Le projet est bien structuré, clair et respecte les conventions attendues dans un développement Python professionnel. Toutes les fonctionnalités obligatoires et avancées ont été correctement mises en œuvre, notamment le scan réseau asynchrone et la détection de ports ouverts. Les tests unitaires sont nombreux, bien organisés et couvrent aussi bien les fonctions synchrones que les cas asynchrones, avec une bonne utilisation de `unittest`, `mock` et `AsyncMock`.

🟩 Le pipeline CI/CD répond parfaitement aux attentes : il exécute les tests sur plusieurs versions de Python, vérifie la qualité du code avec `flake8` et `pylint`, mesure la couverture de code avec `coverage`, et génère automatiquement la documentation Sphinx. Cette documentation est structurée et accessible depuis GitHub Pages.

🟦 Cependant, certains points peuvent encore être améliorés. Le fichier `README.md` pourrait être enrichi avec des badges d’intégration continue, une illustration du rendu de la documentation, et quelques exemples d’utilisation visuelle.  
Par ailleurs, bien que le scan des ports soit fonctionnel avec `nmap`, l’intégration d’une solution en pur Python aurait rendu le projet plus portable.  
Enfin, il pourrait être intéressant d’ajouter un système d’installation (comme un `setup.py` ou un `pyproject.toml`), ainsi que des tests d’intégration simulant des scénarios plus proches d’un environnement réel.

🟩 Ce projet m’a permis de renforcer mes compétences sur la structuration propre d’un projet Python, et plus globalement sur l’organisation d’un dépôt Git. J’ai également consolidé mes connaissances en intégration continue avec GitHub Actions, en documentation technique avec Sphinx, en écriture de tests unitaires avancés (y compris pour des fonctions asynchrones), et en conception d’outils réseau fiables, maintenables et bien documentés.


### 💪 Ce que j’ai appris

- L’usage avancé de `unittest`, notamment pour les cas asynchrones.
- La structuration propre d’un projet Python et plus globalement sur git avec séparation claire des responsabilités.
- La configuration de CI/CD avec GitHub Actions, et l’importance de l’automatisation.
- L’utilisation de `sphinx` pour documenter proprement un code Python complexe.
- L’écriture de code réutilisable, testable et lisible.
