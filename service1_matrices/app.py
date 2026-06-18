from flask import Flask, request, jsonify
import numpy as np

# Création de l'application Flask
app = Flask(__name__)

def parse_matrix(data, key):
    """
    Récupère une matrice depuis le JSON
    et la convertit en tableau NumPy.
    """
    try:
        return np.array(data[key], dtype=float)
    except (KeyError, ValueError) as e:
        raise ValueError(f"Matrice '{key}' invalide : {e}")


# Route POST pour additionner deux matrices
@app.route('/matrices/add', methods=['POST'])
def add_matrices():

    # Lecture du JSON envoyé par le client
    data = request.get_json()
    print(data)
    try:
        # Récupération des matrices A et B
        A = parse_matrix(data, 'A')
        B = parse_matrix(data, 'B')
        print(A)
        print(B)
        # Vérification : mêmes dimensions obligatoires
        if A.shape != B.shape:
            return jsonify({'erreur': 'Dimensions incompatibles'}), 400

        # Calcul de l'addition
        result = (A + B).tolist()

        return jsonify({
            'operation': 'addition',
            'resultat': result
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400



# Route POST pour multiplier deux matrices
@app.route('/matrices/multiply', methods=['POST'])
def multiply_matrices():

    data = request.get_json()

    try:
        A = parse_matrix(data, 'A')
        B = parse_matrix(data, 'B')

        # Vérification : Colonnes(A) = Lignes(B)
        if A.shape[1] != B.shape[0]:
            return jsonify({
                'erreur': 'Colonnes(A) doit egaler Lignes(B)'
            }), 400

        # Produit matriciel avec NumPy
        result = np.dot(A, B).tolist()

        return jsonify({
            'operation': 'multiplication',
            'resultat': result
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


# Route POST pour calculer la transposée
@app.route('/matrices/transpose', methods=['POST'])
def transpose_matrix():

    data = request.get_json()

    try:
        A = parse_matrix(data, 'A')

        # A.T = transposée de la matrice
        result = A.T.tolist()

        return jsonify({
            'operation': 'transposee',
            'resultat': result
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


# Route POST pour calculer le déterminant
@app.route('/matrices/determinant', methods=['POST'])
def determinant_matrix():

    data = request.get_json()

    try:
        A = parse_matrix(data, 'A')

        # Le déterminant n'existe que pour une matrice carrée
        if A.shape[0] != A.shape[1]:
            return jsonify({
                'erreur': 'La matrice doit etre carree'
            }), 400

        # Calcul du déterminant
        det = np.linalg.det(A)

        return jsonify({
            'operation': 'determinant',
            'resultat': round(det, 6)
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


# Route POST pour calculer l'inverse
@app.route('/matrices/inverse', methods=['POST'])
def inverse_matrix():

    data = request.get_json()

    try:
        A = parse_matrix(data, 'A')

        # Une matrice doit être carrée pour être inversible
        if A.shape[0] != A.shape[1]:
            return jsonify({
                'erreur': 'La matrice doit etre carree'
            }), 400

        # Calcul du déterminant
        det = np.linalg.det(A)

        # Si det = 0, la matrice est singulière
        if abs(det) < 1e-10:
            return jsonify({
                'erreur': 'Matrice singuliere, non inversible'
            }), 400

        # Calcul de l'inverse
        result = np.linalg.inv(A).tolist()

        return jsonify({
            'operation': 'inverse',
            'resultat': result
        })

    except (ValueError, TypeError) as e:
        return jsonify({'erreur': str(e)}), 400


# Lancement du serveur Flask
if __name__ == '__main__':
    app.run(debug=True, port=5001)