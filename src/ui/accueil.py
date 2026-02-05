import streamlit as st
from src.core.treasure import *
import requests
import pandas as pd

# Configurer la mise en page de la page Streamlit pour qu'elle soit large
st.set_page_config(layout="wide",
    page_title="Fruit Manager",
    page_icon="./fruit-manager-logo.svg"
)


# VARIABLE
PATH_LOGO = "./fruit-manager-logo.svg"
API_URL = "http://127.0.0.1:8000"

# Importation des données
tresorerie = ouvrir_tresorerie()
if "inventaire" not in st.session_state:
    st.session_state.inventaire = {i['name']:i["quantite"] for i in requests.get(f"{API_URL}/inventaire").json()}
if "history" not in st.session_state:
    st.session_state.history = requests.get(f"{API_URL}/history/").json()
if "API_URL" not in st.session_state:
    st.session_state.API_URL = API_URL

####################

# Sidebar

####################

with st.sidebar:
    # Vente des fruits
    st.title("🛒 Vendre des Fruits")
    sell_fruit = st.selectbox("Choisir un fruit à vendre", [key for key, value in st.session_state.inventaire.items() if value > 0]) 
    sell_number = st.number_input("Quantité à vendre",1, st.session_state.inventaire.get(sell_fruit,0))
    sell_button = st.button("Vendre")
    
    if sell_button: 
        data = {
        "name_fruit": sell_fruit,
        "quantite": sell_number
        }
        total = requests.post(f"{API_URL}/inventaire/vente/",json = data).json()
        tresorerie += total
        ecrire_tresorerie(tresorerie)
        
        # Mettre à jour session_state
        st.session_state.inventaire = {i['name']: i["quantite"] for i in requests.get(f"{API_URL}/inventaire").json()}
        
        # Màj historique
        st.session_state.history = requests.get(f"{API_URL}/history/").json() 
        
        
    # Récolte des Fruits
    st.title("🌱 Récolter des Fruits")
    harvest_fruits = st.selectbox("Choisir un fruit", [key for key in st.session_state.inventaire.keys()]) 
    harvest_number = st.number_input("Quantité à récolter",0,100)
    harvest_fruit = st.button("Récolter")
    if harvest_fruit:
        
        response = requests.put(f"{API_URL}/inventaire/recolte/{harvest_fruits}",params={'value':harvest_number}).json()

        # Mettre à jour session_state
        st.session_state.inventaire = {i['name']: i["quantite"] for i in requests.get(f"{API_URL}/inventaire").json()}
        
        # Màj historique
        st.session_state.history = requests.get(f"{API_URL}/history/").json() 

#####################################

# DASHBOARD

#####################################
st.markdown("---")
st.markdown(f"""<div align="center">
    <img src="https://raw.githubusercontent.com/gdutr/fruit-manager/63cd361f5b5e4789f25832367a2515a7e1732a67/fruit-manager-logo.svg" alt="Logo" height="150" width="2100">
</div>""", unsafe_allow_html=True)
st.markdown("___")

st.title("🍇 Dashboard de la plantation")

st.header("💰 Trésorerie")
tresorerie = ouvrir_tresorerie()
st.metric(label="Montant disponible", value=f"{tresorerie:.2f} €")

st.header("📦 Inventaire")
st.table(st.session_state.inventaire)

st.header("📋 Historique")

st.table(st.session_state.history )