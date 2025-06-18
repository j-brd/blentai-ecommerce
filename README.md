# API Auth - FastAPI

Une API d'authentification pour la solution E-Commerce

## 🗂 Structure du projet
your_project/
├── .env # Fichier de config environnement
├── app/
│ ├── main.py # Entrée de l'app
│ ├── core/ # Config, DB, sécurité
│ ├── models/ # Modèles SQLAlchemy
│ ├── routers/ # Routes (auth, user...)
│ ├── schemas/ # Schémas Pydantic
│ └── services/ # Logique métier
├── requirements.txt # Dépendances
└── README.md # Ce fichier

## ⚙ Pré-requis
- Python 3.9 ou supérieur
- pip

## 🚀 Installation
1️ Clone le repo :
```
bash
git clone <your-repo-url>
cd your_project
```

2 Installe les dépendances :
pip install -r requirements.txt

3 Prépare ton fichier .env :
SECRET_KEY=supersecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

4 initialise la base : 
python -m scripts.init_db

4 Lance le serveur : 
python -m uvicorn app.main:app --reload --port 10000

## Endpoints principaux
POST /api/auth/register → Inscription d'un nouvel utilisateur (retourne un token)
POST /api/auth/login → Connexion (retourne un token)
La doc interactive est disponible ici : http://127.0.0.1:8000/docs

