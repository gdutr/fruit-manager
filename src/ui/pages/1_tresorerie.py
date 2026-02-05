import streamlit as st
# from my_package.fruit_manager import *
import requests
import pandas as pd

# IMPORTATION DES DONNEES
df = pd.DataFrame(st.session_state.history)

st.header("Bienvenue dans la section trésorerie")

# KPI DEPUIS LA CREATION
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Chiffre d'affaires total", f"{df['prix_total'].sum():.2f} €")
with col2:
    st.metric("Nombre de ventes", len(df))
with col3:
    st.metric("Panier moyen", f"{df['prix_total'].mean():.2f} €")
with col4:
    st.metric("Fruits vendus", df['nombre'].sum())

# SEPARATION
st.markdown('___')
st.subheader("📈 Évolution du chiffre d'affaires")
daily_sales = df.groupby('date')['prix_total'].sum().reset_index()
st.line_chart(daily_sales.set_index('date'))

st.markdown('___')

# TOP DES FRUITS LES PLUS VENDU
st.subheader("🏆 Top des fruits")
col1, col2 = st.columns(2)

with col1:
    st.write("**Par quantité**")
    top_qty = df.groupby('name_fruit')['nombre'].sum().sort_values(ascending=False)
    st.bar_chart(top_qty)

with col2:
    st.write("**Par chiffre d'affaires**")
    top_ca = df.groupby('name_fruit')['prix_total'].sum().sort_values(ascending=False)
    st.bar_chart(top_ca)

st.markdown("___")

# STATISTIQUE PAR FRUIT
st.subheader("📋 Statistiques par fruit")
stats = df.groupby('name_fruit').agg({
    'nombre': ['sum', 'mean'],
    'prix_total': ['sum', 'mean'],
    'id': 'count'  
}).round(2)
stats.columns = ['Quantité totale', 'Qté moyenne/vente', 'CA total', 'CA moyen/vente', 'Nb ventes']
st.dataframe(stats)