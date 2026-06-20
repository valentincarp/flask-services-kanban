# Service 2 — Fonctions Statistiques

## Description
API REST Flask permettant d'effectuer des calculs statistiques sur des données passées en JSON.
Utilise Flask, NumPy et SciPy.

## Installation
```bash
cd service2_statistiques
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Routes disponibles

### POST /stats/describe
Calcule les statistiques descriptives d'un tableau de valeurs.

**Corps de la requête (JSON) :**
```json
{"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]}
```

**Réponse (200 OK) :**
```json
{
  "operation": "description",
  "resultat": {
    "n": 8,
    "moyenne": 13.6875,
    "mediane": 12.85,
    "ecart_type": 4.1176,
    "variance": 16.9547,
    "minimum": 8.7,
    "maximum": 21.0,
    "q1": 10.525,
    "q3": 16.575,
    "etendue": 12.3
  }
}
```

**Erreurs possibles :** 400 si données manquantes ou invalides.

---

### POST /stats/correlation
Calcule le coefficient de corrélation de Pearson entre deux séries.

**Corps de la requête (JSON) :**
```json
{"x": [1, 2, 3, 4, 5], "y": [2, 4, 5, 4, 5]}
```

**Réponse (200 OK) :**
```json
{
  "operation": "correlation_pearson",
  "resultat": {
    "r": 0.9139,
    "p_value": 0.030385,
    "interpretation": "forte",
    "significatif": true
  }
}
```

**Erreurs possibles :** 400 si x et y n'ont pas la même longueur.

---

### POST /stats/test_normalite
Effectue le test de Shapiro-Wilk pour vérifier si une série suit une loi normale.

**Corps de la requête (JSON) :**
```json
{"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]}
```

**Réponse (200 OK) :**
```json
{
  "operation": "test_normalite_shapiro_wilk",
  "resultat": {
    "statistique": 0.976,
    "p_value": 0.932,
    "est_normale": true,
    "interpretation": "Distribution normale (p > 0.05)"
  }
}
```

**Erreurs possibles :** 400 si moins de 2 valeurs, 400 si plus de 5000 valeurs.

---

### POST /stats/test_student
Compare les moyennes de deux groupes indépendants (test t de Student).

**Corps de la requête (JSON) :**
```json
{"groupe1": [12.5, 15.3, 8.7], "groupe2": [21.0, 13.2, 9.8]}
```

**Réponse (200 OK) :**
```json
{
  "operation": "test_t_student",
  "resultat": {
    "t_statistique": -0.5123,
    "p_value": 0.632,
    "difference_significative": false
  }
}
```

## Codes HTTP
| Code | Signification |
|------|--------------|
| 200  | Succès |
| 400  | Données invalides ou paramètre manquant |
| 500  | Erreur serveur interne |

## Port
Le service tourne sur le port **5002**.
```bash
curl -X POST http://localhost:5002/stats/describe \
     -H 'Content-Type: application/json' \
     -d '{"data": [12.5, 15.3, 8.7, 21.0]}'
```