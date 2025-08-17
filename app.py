import streamlit as st
from my_package.fruit_manager import *

# Configurer la mise en page de la page Streamlit pour qu'elle soit large
# st.set_page_config(layout="wide")

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