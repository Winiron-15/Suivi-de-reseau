# Projet choisi : Suivi-de-reseau

Ce projet permet de scanner un réseau local à partir :
- d'un fichier CSV contenant des IPs et noms de machines
- ou d'une plage IP en notation CIDR (ex : 192.168.1.0/24)

Les machines actives sont pingées, et leurs noms d'hôtes sont récupérés si possible grâce à `nmap`.

## 📦 Prérequis

### Python

- Python 3.7+

### Dépendances Python

Installez les dépendances Python avec :

```bash
pip install -r requirements.txt
```

### Outil système requis : `nmap`

#### ✅ Linux (Debian/Ubuntu) :

```bash
sudo apt update
sudo apt install nmap
```

#### 🍏 macOS :

```bash
brew install nmap
```

#### 🪟 Windows :

1. Téléchargez l’installeur ici : [https://nmap.org/download.html](https://nmap.org/download.html)
2. Pendant l’installation, cochez **“Add Nmap to the system PATH”**
3. Redémarrez votre terminal (cmd ou PowerShell)

---

## ▶️ Utilisation

### Scanner à partir d'un fichier CSV

```bash
python src/main.py --file machines.csv
```

### Scanner une plage IP CIDR

```bash
python src/main.py --range 192.168.2.0/24
```

Les résultats seront enregistrés dans :
- `data/results.csv` (si `--file`)
- `scan-results.csv` (si `--range`)





- Une description du projet.
- Les commandes d’utilisation (avec exemples).
- Les dépendances nécessaires (si utilisées).