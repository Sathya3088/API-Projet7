from joblib import load
from fastapi import FastAPI
import pandas as pd
import numpy as np

dataframe = pd.read_csv('data/df.csv')
app = FastAPI()

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

    return {"client_id": client_id, "probability": predicted_probability, "decision" : decision}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
