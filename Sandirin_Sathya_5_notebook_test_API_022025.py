import pytest
from fastapi.testclient import TestClient
from Sandirin_Sathya_1_API_022025 import app

client = TestClient(app)

# Vous devriez déjà avoir df.csv chargé dans un environnement de test
# Voici des exemples d'IDs que vous pourriez créer pour simuler les données
# Assurez-vous que ces IDs existent et ont des valeurs correspondantes dans votre fichier CSV

def test_predict_client_accepted():
    response = client.get("/predict/100002")  # ID de client qui sera accepté
    assert response.status_code == 200
    assert response.json()['decision'] == "Crédit accepté"

def test_predict_client_refused():
    response = client.get("/predict/100007")  # ID de client qui sera refusé
    assert response.status_code == 200
    assert response.json()['decision'] == "Crédit refusé"

def test_predict_client_not_found():
    response = client.get("/predict/456260")  # ID de client qui n'existe pas
    assert response.status_code == 404
    assert response.json() == {"error": "Client ID not found"}
