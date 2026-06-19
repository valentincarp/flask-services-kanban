from flask import Flask, request, jsonify
import pandas as pd
from dotenv import load_dotenv
import mysql.connector
import os
import io

# Charge les variables du fichier .env
load_dotenv()

# Création de l'application Flask
app = Flask(__name__)

# Colonnes obligatoires dans le CSV
COLONNES_REQUISES = {'nom_serie', 'valeur'}

# Colonnes autorisées
COLONNES_VALIDES = {'nom_serie', 'valeur', 'categorie', 'date_mesure'}

# Taille maximale du fichier : 5 Mo
TAILLE_MAX_OCTETS = 5 * 1024 * 1024

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )



# Route principale d'upload CSV
@app.route('/upload/csv', methods=['POST'])
def upload_csv():

    # Vérifie qu'un fichier a été envoyé
    if 'file' not in request.files:
        return jsonify({
            'erreur': 'Aucun fichier envoyé (clé "file" manquante)'
        }), 400

    # Récupération du fichier
    file = request.files['file']

    # Vérifie que le nom du fichier n'est pas vide
    if file.filename == '':
        return jsonify({
            'erreur': 'Nom de fichier vide'
        }), 400

    # Vérifie que le fichier est bien un CSV
    if not file.filename.endswith('.csv'):
        return jsonify({
            'erreur': 'Seuls les fichiers .csv sont acceptés'
        }), 400

    # Lecture du contenu du CSV
    try:
        content = file.read()

        # Vérifie la taille maximale
        if len(content) > TAILLE_MAX_OCTETS:
            return jsonify({
                'erreur': 'Fichier trop volumineux (max 5 Mo)'
            }), 413

        # Chargement du CSV dans un DataFrame pandas
        df = pd.read_csv(io.BytesIO(content))

    except Exception as e:
        return jsonify({
            'erreur': f'Lecture CSV impossible : {e}'
        }), 400

    # Vérifie que les colonnes obligatoires existent
    colonnes_manquantes = COLONNES_REQUISES - set(df.columns)

    if colonnes_manquantes:
        return jsonify({
            'erreur': 'Colonnes obligatoires manquantes',
            'manquantes': list(colonnes_manquantes)
        }), 400

    # Garde uniquement les colonnes autorisées
    df = df[[c for c in df.columns if c in COLONNES_VALIDES]]

    # Convertit la colonne valeur en nombre
    # Les valeurs incorrectes deviennent NaN
    df['valeur'] = pd.to_numeric(
        df['valeur'],
        errors='coerce'
    )

    # Compte les lignes invalides
    lignes_invalides = df['valeur'].isna().sum()

    # Supprime les lignes dont la valeur est invalide
    df.dropna(
        subset=['valeur'],
        inplace=True
    )

    # Vérifie qu'il reste au moins une ligne valide
    if df.empty:
        return jsonify({
            'erreur': 'Aucune ligne valide dans le CSV'
        }), 400
        
    # insérer dans mysql
    try : 
        
        conn = get_connection()
        cursor = conn.cursor()
        
        insertions = 0
        
        for _, row in df.iterrows():
            
            cursor.execute(
                'INSERT INTO donnees (nom_serie, valeur, categorie, date_mesure)'
                ' VALUES (%s, %s, %s, %s)',
                (
                    str(row['nom_serie']),
                    float(row['valeur']),
                    str(row['categorie']) if 'categorie' in df.columns else None,
                     str(row['date_mesure']) if 'date_mesure' in df.columns else None,
                    
                    
                )
            )
            
            insertion += 1
        conn.commit()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        
        return jsonify({
            'erreur': 'Erreur base de donnée',
            'detail': str(e)
        }), 500
        
    return jsonify({
        'statut': 'success',
        'lignes_inserees': insertions,
        'lignes_invalides_ignorees': int(lignes_invalides),
        'message': f'{insertions} ligne(s) chargée(s) dans la table donnees'
        
    }), 201

# Lancement du serveur Flask sur le port 5004
if __name__ == '__main__':
    app.run(debug=True, port=5004)