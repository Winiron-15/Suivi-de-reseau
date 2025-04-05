Utilisation de l'outil
======================

Le projet **Suivi de Réseau** permet d'effectuer des analyses réseau à l'aide de la ligne de commande.
Vous pouvez scanner des adresses IP en les listant dans un fichier CSV ou en spécifiant une plage IP
au format CIDR. L'outil vous offre également le choix entre un scan multithreadé (par défaut) ou
asynchrone, ainsi que l'option de détecter les ports ouverts avec `nmap`.

Commandes disponibles
---------------------

1. **Scanner un fichier CSV de machines**

Le fichier CSV doit contenir au moins deux colonnes : le nom de la machine et son IP.

Exemple de fichier : `data/machines.csv`

.. code-block:: bash

    Nom,IP
    Serveur1,192.168.1.10
    Routeur,192.168.1.1

Commande :

.. code-block:: bash

    python src/main.py --file data/machines.csv

2. **Scanner une plage IP au format CIDR**

.. code-block:: bash

    python src/main.py --range 192.168.1.0/24

3. **Activer le scan des ports TCP ouverts avec nmap**

Cette option ajoute un scan complet des ports 1 à 65535 sur les hôtes détectés comme actifs.

.. code-block:: bash

    python src/main.py --range 192.168.1.0/24 --ports

4. **Utiliser la version asynchrone pour de meilleures performances**

.. code-block:: bash

    python src/main.py --file data/machines.csv --async

5. **Contrôler le nombre de threads (pour le mode multithreadé uniquement)**

Par défaut, l'outil utilise 10 threads pour exécuter les pings en parallèle.
Vous pouvez ajuster ce nombre avec `--threads`.

.. code-block:: bash

    python src/main.py --range 192.168.1.0/24 --threads 20

    python src/main.py --file data/machines.csv --threads 5

Résumé des options disponibles
------------------------------

- `--file` : Fichier CSV à utiliser comme source d'IP
- `--range` : Plage IP au format CIDR à scanner
- `--ports` : Active le scan complet des ports (via nmap)
- `--async` : Utilise la version asynchrone (sinon multithreadé)
- `--threads` : Nombre de threads à utiliser (si mode multithread)

