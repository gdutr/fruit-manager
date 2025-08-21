import streamlit as st
from my_package.fruit_manager import *
import requests
import pandas as pd

# Configurer la mise en page de la page Streamlit pour qu'elle soit large
# st.set_page_config(layout="wide")


button_api = st.sidebar.toggle("API")

if not button_api:

    # Importation des données
    inventaire = ouvrir_inventaire()
    prix = ouvrir_prix()
    tresorerie = ouvrir_tresorerie()

    ####################

    # Sidebar

    ####################

    with st.sidebar:
        # Vente des fruits
        st.title("🛒 Vendre des Fruits")
        sell_fruit = st.selectbox("Choisir un fruit à vendre", [key for key, value in inventaire.items() if value > 0]) 
        sell_number = st.number_input("Quantité à vendre",1, inventaire.get(sell_fruit,0))
        sell_button = st.button("Vendre")
        
        if sell_button: 
            inventaire, tresorerie = vendre(inventaire, sell_fruit, sell_number, tresorerie, prix)
            
            ecrire_inventaire(inventaire)
            ecrire_tresorerie(tresorerie)
            
            st.success(f"La vente des {sell_fruit} vous à remporté {sell_number*prix.get(sell_fruit)}€",icon='🔥')
            
            
        # Récolte des Fruits
        st.title("🌱 Récolter des Fruits")
        harvest_fruits = st.selectbox("Choisir un fruit", [key for key in inventaire.keys()]) 
        harvest_number = st.number_input("Quantité à récolter",0,100)
        harvest_fruit = st.button("Récolter")
        if harvest_fruit:
            recolter(inventaire, harvest_fruits, harvest_number)
            ecrire_inventaire(inventaire)


    #####################################

    # DASHBOARD

    #####################################

    st.title("🍇 Dashboard de la plantation")

    st.header("💰 Trésorerie")
    tresorerie = ouvrir_tresorerie()
    st.metric(label="Montant disponible", value=f"{tresorerie:.2f} €")

    st.header("📦 Inventaire")
    st.table(inventaire)

    API_URL = "http://127.0.0.1:8000"
    response = requests.get(f"{API_URL}/inventaire/")

else:
    
    # VARIABLE
    API_URL = "http://127.0.0.1:8000"
    
    # Importation des données
    tresorerie = ouvrir_tresorerie()
    if "inventaire" not in st.session_state:
        st.session_state.inventaire = {i['name']:i["quantite"] for i in requests.get(f"{API_URL}/inventaire").json()}
    if "history" not in st.session_state:
        st.session_state.history = requests.get(f"{API_URL}/history/").json()    

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
            
            
        # Récolte des Fruits
        st.title("🌱 Récolter des Fruits")
        harvest_fruits = st.selectbox("Choisir un fruit", [key for key in st.session_state.inventaire.keys()]) 
        harvest_number = st.number_input("Quantité à récolter",0,100)
        harvest_fruit = st.button("Récolter")
        if harvest_fruit:
            
            response = requests.put(f"{API_URL}/inventaire/recolte/{harvest_fruits}",params={'value':harvest_number}).json()

            # Mettre à jour session_state
            st.session_state.inventaire = {i['name']: i["quantite"] for i in requests.get(f"{API_URL}/inventaire").json()}

    #####################################

    # DASHBOARD

    #####################################

    st.title("🍇 Dashboard de la plantation")

    st.header("💰 Trésorerie")
    tresorerie = ouvrir_tresorerie()
    st.metric(label="Montant disponible", value=f"{tresorerie:.2f} €")

    st.header("📦 Inventaire")
    st.table(st.session_state.inventaire)
    
    st.header("📋 Historique")
    
    
    st.session_state.history = requests.get(f"{API_URL}/history/").json() 
    st.table(st.session_state.history )