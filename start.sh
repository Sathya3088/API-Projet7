#!/bin/bash

# Mise à jour des paquets
apt-get update

# Installation des dépendances
apt-get -y install curl
apt-get -y install python3-distutils
uvicorn Sandirin_Sathya_1_API_022025:app --host 0.0.0.0 --port 8000 --reload
