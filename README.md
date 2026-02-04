# 🍇 Fruit Manager
Application de gestion d'inventaire et de ventes de fruits avec suivi de trésorerie et analyse de saisonnalité.

## 📋 Description

Fruit Manager est une application complète permettant de :
- Gérer l'inventaire des fruits (récoltes et stocks)
- Enregistrer et suivre les ventes
- Monitorer la trésorerie en temps réel
- Visualiser la saisonnalité des fruits et légumes
- Consulter les données via une API REST

## 🚀 Fonctionnalités

- **API REST (FastAPI)** : Interface pour toutes les opérations CRUD
- **Interface utilisateur (Streamlit)** : Dashboard interactif avec 2 pages principales
  - Page Trésorerie : Suivi financier et historique des transactions
  - Page Saisonnalité : Visualisation des fruits de saison
- **Base de données SQLite** : Stockage persistant des données
- **Web Scraping** : Récupération automatique des informations de saisonnalité

## 🛠️ Technologies utilisées

- **Backend** : Python 3.9+, FastAPI, SQLAlchemy, Pydantic
- **Frontend** : Streamlit
- **Base de données** : SQLite
- **Scraping** : BeautifulSoup4, Requests 
- **Gestion de dépendances** : Poetry

## 📁 Structure du projet
```text
fruit-manager/
├── data/                         # Données et base de données
│   ├── database.db               # Base SQLite (inventaire, ventes, prix)
│   ├── seasons_fruits_legs.json  # Données de saisonnalité scrappées
│   ├── list_fruits.json          # Liste filtrée des fruits uniquement
│   └── tresorerie.txt            # Fichier de suivi de trésorerie
│
├── src/                      # Code source principal
│   ├── core/                 # Logique métier
│   │   ├── database.py       # Configuration SQLAlchemy
│   │   ├── models.py         # Modèles de données (tables SQL)
│   │   ├── schemas.py        # Schémas Pydantic pour validation
│   │   └── treasury.py       # Gestion de la trésorerie
│   │
│   ├── api/                  # API REST
│   │   └── main.py           # Point d'entrée FastAPI avec routes
│   │
│   ├── ui/                   # Interface Streamlit
│   │   └── pages/
│   │       ├── 1_tresorerie.py    # Page de suivi financier
│   │       └── 2_saisonnalite.py  # Page d'analyse saisonnière
│   │
│   └── scraping/                     # Web scraping
│       └── fruits_legumes_season.py  # Script de collecte de données
│
├── run.py                    # Lanceur combiné (API + Streamlit)
├── poetry.lock               # Versions exactes (Poetry)
├── pyproject.toml            # Configuration Poetry et dépendances
├── requirements.txt          # Dépendances pour pip (généré depuis Poetry)
└── README.md                 # Ce fichier
```

## 🔧 Installation

### Prérequis
- Python 3.12 ou supérieur
- Poetry

---

### Option 1 : Installation avec Poetry (recommandé)

1. **Installer Poetry** (si pas encore installé)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. **Cloner le repository**
```bash
git clone https://github.com/gdutr/fruit-manager.git
cd fruit-manager
```

3. **Installer les dépendances**
```bash
poetry install
```

4. **Activer l'environnement virtuel**
```bash
poetry shell
```

---

### Option 2 : Installation avec pip (sans Poetry)

1. **Cloner le repository**
```bash
git clone https://github.com/gdutr/fruit-manager.git
cd fruit-manager
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**

   **Sur Linux/Mac :**
```bash
   source venv/bin/activate
```

   **Sur Windows :**
```bash
   venv\Scripts\activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Initialiser la base de données** (si nécessaire)
```bash
python scripts/init_database.py
```


---
## 🚀 Utilisation

### Lancement rapide (API + Interface)
```bash
python run.py
```

Cette commande lance simultanément :
- L'API FastAPI sur `http://localhost:8000`
- L'interface Streamlit sur `http://localhost:8501`

### Lancement séparé

**API uniquement :**
```bash
uvicorn src.fruit_manager.api.main:app --reload
```

**Interface Streamlit uniquement :**
```bash
streamlit run src/fruit_manager/ui/app.py
```

### Documentation de l'API

Une fois l'API lancée, accédez à la documentation interactive :
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

## 📊 Fonctionnalités détaillées

### Gestion de l'inventaire
- Ajout de récoltes
- Suivi des stocks en temps réel
- Historique des mouvements

### Gestion des ventes
- Enregistrement des ventes
- Calcul automatique du chiffre d'affaires
- Mise à jour de la trésorerie

### Analyse de saisonnalité
- Visualisation des fruits de saison
- Données mises à jour par web scraping
- Aide à la planification des achats

## 🔮 Améliorations futures

- [ ] Ajout de la gestion des légumes
- [ ] Mise à jour des prix sur le marché actuel
- [ ] Système d'alertes de stock bas
- [ ] Tableau de bord avec KPIs avancés
- [ ] Authentification utilisateur
- [ ] Tests unitaires et d'intégration


## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**Guillaume DUTREUILH**
- GitHub : [@gdutr](https://github.com/gdutr)
- LinkedIn : [@Guillaume](https://www.linkedin.com/in/guillaume-dutreuilh-/)

## 🙏 Remerciements

- [Machine Learnia](https://www.machinelearnia.com/) pour la formation ML-PRO
- Source des données de saisonnalité : [les fruits et legumes frais](https://www.lesfruitsetlegumesfrais.com/legumes-de-saison)

## ⚖️ Mentions légales

### Web Scraping
Ce projet inclut un script de web scraping (`fruits_legumes_season.py`) 
récupérant des informations publiques sur la saisonnalité des fruits.

**Avertissement** :
- Ce code est fourni à des fins éducatives et de démonstration
- L'utilisation doit respecter les conditions d'utilisation du site source
- L'utilisateur est responsable de l'usage qu'il fait de ce code
- Aucune garantie n'est fournie quant à la légalité de l'usage dans votre juridiction

**Bonnes pratiques** :
- Respectez le fichier robots.txt du site
- Limitez la fréquence des requêtes (rate limiting)
- N'utilisez pas les données à des fins commerciales sans autorisation
- Citez toujours la source des données
---

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !