from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io

app = Flask(__name__)
CORS(app)

COLONNES_REQUISES = {'nom_serie', 'valeur'}


@app.route('/')
def home():
    return "Service 4 CSV -> MySQL"


@app.route('/upload/csv', methods=['POST'])
def upload_csv():

    # Vérifier la présence du fichier
    if 'file' not in request.files:
        return jsonify({
            'erreur': 'Aucun fichier envoyé (clé "file" manquante)'
        }), 400

    file = request.files['file']

    # Vérifier le nom du fichier
    if file.filename == '':
        return jsonify({
            'erreur': 'Nom de fichier vide'
        }), 400

    # Vérifier l'extension
    if not file.filename.endswith('.csv'):
        return jsonify({
            'erreur': 'Seuls les fichiers .csv sont acceptés'
        }), 400

    try:
        # Lire le contenu du fichier
        contenu = file.read()

        # Charger le CSV dans Pandas
        df = pd.read_csv(io.BytesIO(contenu))

        # Vérifier les colonnes obligatoires
        colonnes_manquantes = COLONNES_REQUISES - set(df.columns)

        if colonnes_manquantes:
            return jsonify({
                'erreur': 'Colonnes obligatoires manquantes',
                'manquantes': list(colonnes_manquantes)
            }), 400

        return jsonify({
            'statut': 'success',
            'nom_fichier': file.filename,
            'colonnes': list(df.columns),
            'nombre_colonnes': len(df.columns),
            'nombre_lignes': len(df)
        }), 200

    except Exception as e:
        return jsonify({
            'erreur': f'Lecture CSV impossible : {str(e)}'
        }), 400


if __name__ == '__main__':
    app.run(debug=True, port=5004)