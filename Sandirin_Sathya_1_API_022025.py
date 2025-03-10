from joblib import load
from fastapi import FastAPI
import pandas as pd
import numpy as np
import shap
from fastapi.middleware.cors import CORSMiddleware

dataframe = pd.read_csv('data/df.csv')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle :
model = load("model.joblib")
print(type(model))

@app.get("/predict/{client_id}")
def predict(client_id: int):
    client_data = dataframe[dataframe['SK_ID_CURR'] == client_id]

    if client_data.empty:
        return {"error": "Client ID not found"}, 404  # Gestion d'erreur si le client n'est pas trouvé

    features = client_data.drop(['TARGET', 'SK_ID_CURR', 'index'], axis=1).values
    prediction = model.predict_proba(features)  # La probabilité

    # Définition du seuil
    threshold = 0.6  
    predicted_probability = prediction[0][1]
    decision = "Crédit accepté" if predicted_probability >= threshold else "Crédit refusé"

    # Récupérer les valeurs SHAP pour le client
    client_features = client_data.drop(['TARGET', 'SK_ID_CURR', 'index'], axis=1)
    assert client_features.shape[1] == 795, "Le nombre de features doit être de 795."

    explainer = shap.Explainer(model)
    shap_values = explainer(client_features.values)
    shap_values_list = shap_values.values.tolist()

    return {"client_id": client_id, "probability": predicted_probability, "decision" : decision, "shap_values": shap_values_list}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
