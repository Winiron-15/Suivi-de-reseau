## 🧱 Architecture complète du projet

```
SUIVI-DE-RESEAU/
├── .github/
│   └── workflows/
│       ├── deploy-doc.yml     # Déploie automatiquement la documentation (GitHub Pages, etc.)
│       ├── pep8.yml           # Vérifie la conformité PEP8 (flake8/pylint)
│       └── tests.yml          # Exécute les tests unitaires et mesure la couverture
│
├── data/
│   ├── machines.csv           # Liste des machines/IP à scanner
│   └── results/
│       ├── file-results.csv   # Résultats si input via CSV
│       └── range-results.csv  # Résultats si input via plage IP (--range)
│
├── docs/
│   ├── source/
│   │   ├── arguments.rst      # Doc pour le parsing CLI
│   │   ├── conf.py            # Config Sphinx
│   │   ├── core.rst           # Doc pour modules src/core/
│   │   ├── index.rst          # Page d’accueil
│   │   ├── main.rst           # Doc du script principal
│   │   ├── usage.rst          # Guide d’utilisation
│   │   └── utils.rst          # Doc pour les utilitaires
│   ├── make.bat               # Build doc (Windows)
│   └── Makefile               # Build doc (Linux/Mac)
│
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── ping.py            # Génère commande ping selon OS
│   │   ├── port_scanner.py    # Scan tous les ports TCP via nmap
│   │   ├── runner.py          # Coordonne les différents types de scans
│   │   ├── scanner_async.py   # Ping réseau en async avec asyncio
│   │   └── scanner_threaded.py# Ping multithreadé
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── csv_utils.py       # Lecture/écriture CSV
│   │   ├── logger.py          # Logger custom
│   │   └── parsing.py         # Extraction latence + DNS reverse
│   ├── __init__.py
│   ├── arguments.py           # Parsing CLI avec argparse
│   └── main.py                # Point d'entrée de l'outil en ligne de commande
│
├── tests/
│   ├── test_arguments.py
│   ├── test_core_ping.py
│   ├── test_core_port_scanner.py
│   ├── test_core_runner.py
│   ├── test_core_scanner_async.py
│   ├── test_core_scanner_threaded.py
│   ├── test_main.py
│   ├── test_utils_csv_utils.py
│   └── test_utils_parsing.py
│   # Chaque module dans src/ a un fichier de test correspondant
│
├── .gitignore                # Fichiers/dossiers ignorés par Git (cache, venv, etc.)
└── README.md                 # Présentation du projet, instructions, etc.