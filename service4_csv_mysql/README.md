# Service 4 - CSV vers MySQL

## Description

Service Flask permettant :

* l'upload d'un fichier CSV
* la validation des données
* la lecture du fichier avec Pandas
* la préparation de l'insertion des données dans MySQL

Port utilisé :

5004

---

## Installation

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Lancer le service :

```bash
python app.py
```

Le serveur démarre sur :

```text
http://127.0.0.1:5004
```

---

## Route disponible

### POST /upload/csv

Permet d'envoyer un fichier CSV.

URL :

```text
http://127.0.0.1:5004/upload/csv
```

Méthode :

```text
POST
```

Champ attendu :

```text
file
```

Extension acceptée :

```text
.csv
```

---

## Colonnes obligatoires

```text
nom_serie
valeur
```

Colonnes facultatives :

```text
categorie
date_mesure
```

---

## Exemple de fichier CSV

```csv
nom_serie,valeur,categorie,date_mesure
serie_A,12.50,temperature,2024-01-15
serie_A,15.30,temperature,2024-01-16
serie_B,45.10,pression,2024-01-15
```

---

## Réponse de succès

```json
{
    "statut": "success",
    "nom_fichier": "donnees_exemple.csv",
    "nombre_colonnes": 4,
    "nombre_lignes": 6
}
```

---

## Tests réalisés

### Client Python

```text
test_client.py
```

### Client HTML / JavaScript

```text
test_client.html
```

---

## Auteur

Étudiant D - Service 4
