import pytest
from fastapi.testclient import TestClient
from Sandirin_Sathya_1_API_022025 import app

client = TestClient(app)

def test_predict_client_accepted():
    response = client.get("/predict/100002")  # ID de client qui sera accepté
    assert response.status_code == 200
    assert response.json()['decision'] == "Crédit accepté"

def test_predict_client_refused():
    response = client.get("/predict/100007")  # ID de client qui sera refusé
    assert response.status_code == 200
    assert response.json()['decision'] == "Crédit refusé"
