# 🔍 Projet : Suivi de Réseau

![Tests](https://github.com/winiron-15/Suivi-de-reseau/actions/workflows/tests.yml/badge.svg)
![Docs](https://github.com/winiron-15/Suivi-de-reseau/actions/workflows/deploy-doc.yml/badge.svg)

Ce projet permet de **scanner un réseau local** afin d’identifier les machines actives et de détecter les **ports TCP ouverts** sur celles-ci via `nmap`.

Il peut fonctionner à partir :
- d’un **fichier CSV** contenant les IPs et noms de machines
- ou d’une **plage IP au format CIDR** (ex : `192.168.1.0/24`)

---

## 🧭 Sommaire

- [⚠️ Avertissement légal](#️-avertissement-légal)
- [📦 Prérequis](#-prérequis)
- [🚀 Installation rapide](#-installation-rapide)
- [▶️ Utilisation](#️-utilisation)
- [💾 Résultats](#-résultats)
- [🧱 Architecture du projet](#-architecture-du-projet)
- [📚 Documentation](#-documentation)
- [✍️ Auteur](#️-auteur)

---

## ⚠️ AVERTISSEMENT LÉGAL

> 🔒 **Attention : il est strictement interdit de scanner des adresses IP ou des plages réseau qui ne vous appartiennent pas ou pour lesquelles vous n’avez pas une autorisation explicite.**
>
> Le scan de ports sans autorisation peut être considéré comme une activité malveillante et est **illégal dans de nombreuses juridictions**.
>
> ➤ Utilisez cet outil uniquement **dans un cadre personnel, pédagogique ou professionnel autorisé.**

---

## 🚀 Installation rapide

```bash
git clone https://github.com/winiron-15/Suivi-de-reseau.git
cd Suivi-de-reseau
```
---

## 📦 Prérequis

### ✔️ Python

- Version recommandée : **Python 3.7+**

### ✔️ Outil système requis pour le scan de ports: `nmap`

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

### 🌐 2. Scanner depuis une IP
Une IP seule
```bash
python -m src.main --range 192.168.1.10
```
Une plage IP au format CIDR

```bash
python -m src.main --range 192.168.1.0/24
```

### ⚙️ Options supplémentaires

| Option         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `--threads`    | Définit le nombre de threads pour le scan multithreadé (par défaut : 10).   |
| `--async`      | Active le mode **asynchrone** pour accélérer le scan IP (remplace threading).|
| `--ports`      | Lance un scan complet des **ports TCP (1–65535)** avec `nmap` sur les IP actives. |
| `--file`       | Spécifie un fichier CSV d’entrée contenant les IPs et noms de machines.     |
| `--range`      | Spécifie une plage IP au format CIDR **ou une liste d'IP séparées par des virgules**. |


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
├── .github/workflows/       # CI : tests, lint, déploiement doc
├── data/                    # CSV d'entrée + résultats
├── docs/source/             # Sphinx : .rst + conf.py
├── src/core/ + utils/       # Modules de scan et outils
├── tests/                   # Tests unitaires pour tous les modules
├── main.py                  # Point d’entrée CLI
└── README.md, .gitignore    # Métadonnées projet
```
[Voir le schéma complet ici](structure.md)

---

## 📚 Documentation

La documentation complète est disponible ici :  
👉 [https://winiron-15.github.io/Suivi-de-reseau/](https://winiron-15.github.io/Suivi-de-reseau/)

---
## ✍️ Auteur

Projet réalisé dans le cadre d’un exercice de développement réseau en Python  

📅 Année : 2025  
👨‍🎓 Étudiant : Géraud GAUZINS    
🏫 Établissement : Campus XIIe Avenue