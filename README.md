# 🔍 Projet : Suivi de Réseau

Ce projet permet de **scanner un réseau local** afin d’identifier les machines actives et de détecter les **ports TCP ouverts** sur celles-ci via `nmap`.

Il peut fonctionner à partir :
- d’un **fichier CSV** contenant les IPs et noms de machines
- ou d’une **plage IP au format CIDR** (ex : `192.168.1.0/24`)

---

## ⚠️ AVERTISSEMENT LÉGAL

> 🔒 **Attention : il est strictement interdit de scanner des adresses IP ou des plages réseau qui ne vous appartiennent pas ou pour lesquelles vous n’avez pas une autorisation explicite.**
>
> Le scan de ports sans autorisation peut être considéré comme une activité malveillante et est **illégal dans de nombreuses juridictions**.
>
> ➤ Utilisez cet outil uniquement **dans un cadre personnel, pédagogique ou professionnel autorisé.**

---

## 📦 Prérequis

### ✔️ Python

- Version recommandée : **Python 3.7+**

### ✔️ Outil système requis : `nmap`

#### ✅ Sur Linux (Debian/Ubuntu) :

```bash
sudo apt update
sudo apt install nmap
```

#### 🍏 Sur macOS :

```bash
brew install nmap
```

#### 🪟 Sur Windows :

1. Téléchargez Nmap ici : [https://nmap.org/download.html](https://nmap.org/download.html)
2. Pendant l’installation, cochez **“Add Nmap to the system PATH”**
3. Redémarrez votre terminal (cmd ou PowerShell)

---

## ▶️ Utilisation

### 📁 1. Scanner depuis un fichier CSV

Exemple de fichier `machines.csv` :

```csv
Nom,IP
serveur1,192.168.1.10
serveur2,192.168.1.20
```

Commande :

```bash
python -m src.main --file data/machines.csv
```

### 🌐 2. Scanner une plage IP au format CIDR

```bash
python -m src.main --range 192.168.1.0/24
```

### ⚙️ Options supplémentaires

| Option         | Description                                                    |
|----------------|----------------------------------------------------------------|
| `--threads`    | Nombre de threads utilisés pour le scan (défaut : 10)          |
| `--async`      | Utiliser le scan **asynchrone** plutôt que multithreadé        |
| `--ports`      | Scanner tous les ports TCP (1–65535) sur les hôtes actifs      |

Exemple complet :

```bash
python -m src.main --range 192.168.1.0/24 --async --ports
```

---

## 💾 Résultats

Les résultats sont enregistrés automatiquement dans :
- `data/results/file-results.csv` (si `--file`)
- `data/results/range-results.csv` (si `--range`)

Chaque ligne contient :
```
Nom de machine, IP, Statut, Ping (ms), Ports ouverts
```

---

## 🧱 Architecture du projet

```
SUIVI-DE-RESEAU/
├── .github/
│   └── workflows/
│       ├── deploy-doc.yml
│       ├── pep8.yml
│       └── tests.yml
├── data/
│   ├── machines.csv
│   └── results/
│       ├── file-results.csv
│       └── range-results.csv
├── docs/
│   ├── source/
│   │   ├── arguments.rst
│   │   ├── conf.py
│   │   ├── core.rst
│   │   ├── index.rst
│   │   ├── main.rst
│   │   ├── usage.rst
│   │   └── utils.rst
│   ├── make.bat
│   └── Makefile
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── ping.py
│   │   ├── port_scanner.py
│   │   ├── runner.py
│   │   ├── scanner_async.py
│   │   └── scanner_threaded.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── csv_utils.py
│   │   ├── logger.py
│   │   └── parsing.py
│   ├── __init__.py
│   ├── arguments.py
│   └── main.py
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
├── .gitignore
└── README.md
```
📚 [Consulter la documentation complète](https://winiron-15.github.io/Suivi-de-reseau/)

---

## ✍️ Auteur

Projet réalisé dans le cadre d’un exercice de développement réseau en Python  

📅 Année : 2025  
👨‍🎓 Étudiant : Géraud GAUZINS    
🏫 Établissement : Campus XIIe Avenue