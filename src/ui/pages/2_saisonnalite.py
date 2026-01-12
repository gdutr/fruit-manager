import requests
import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_image_select import image_select
import re

# DECLARATION VARIABLES
dict_emoji ={
    "Cultivé" : "👨‍🌾",
    "Conservation" : "🥫",
    "Àpport": "🍫",
    "Vitamine" : "🏃",
    "À partir de" : "👶",
    "Saison" : "🍂",
    "Pleine saison" : "🌱",
    "Eau" : "💧",
    "Fibres": "🫘",
    # "Vitamine B9": "🏃‍♀️",
    # "Cuivre": "🟫",
    # "Manganèse": "⬛",
    "Glucides": "🍬",
    "Protéines" : "🍗"
    
}

dict_tri_jour_semaine_mois = {
    "Jour" : 0,
    "Semaine" : 1,
    "Mois" : 2
}

tri_flag = False

##########################

# STREAMLIT

##########################
st.set_page_config(layout="wide")
st.markdown("""
# 🍒 Fruits de saison : mangeons au rythme de la nature

Manger des fruits de saison, c’est profiter de produits plus savoureux, plus nutritifs et souvent moins chers, tout en réduisant notre impact environnemental 🌍.
Chaque mois de l’année apporte son lot de couleurs et de saveurs uniques : des fruits gorgés de soleil en été aux variétés riches en vitamines en hiver.

Ce tableau de bord interactif vous permet de :

- Choisir un mois dans l’année 📅

- Découvrir immédiatement les fruits de saison correspondants 🍓🍐🍊

- Explorer pour chaque fruit : son origine, ses apports nutritionnels, ses conseils de conservation et bien plus encore 🍴

👉 Sélectionnez un mois et laissez-vous guider par les fruits que la nature nous offre à ce moment précis.
""")

st.markdown("Les données ont été récupérés sur le site : [les fruits et legumes frais](https://www.lesfruitsetlegumesfrais.com/)\n___",unsafe_allow_html=True)
st.header("Sélectionnez un mois")

# Mois
list_month = ["janvier","fevrier","mars","avril","mai","juin","juillet","aout","septembre","octobre","novembre","decembre"]
API_URL = st.session_state.API_URL


##########################
 
# MAIN

##########################    
choice_month = st.selectbox("Choisissez un mois", list_month)

if choice_month:
    list_fruit = requests.get(f"{API_URL}/seasons/{choice_month}").json().get('fruits',None)
    
    nbre_lignes = len(list_fruit)//5
    
    # rangement par ordre alphabétique
    list_fruit = sorted(list_fruit, key = lambda x: x['nom'])


#############################

# SIDEBAR

#############################
list_cultivation = list()
list_bebe = list()
list_conservation = list()
list_apport = list()
list_eau = list()

for fruit in list_fruit:
    if fruit['description']:
        # ORIGINE CULTIVATION
        value = fruit['description'].get("Cultivé","")
        if value:
            # split des differentes origines
            list_value = [pays.replace(",","") for pays in value.split(" ") if pays not in [',', 'en', "En", "et"]]
            # suppression des espaces en début et fin de mot
            list_value = map(str.strip,list_value)
            list_cultivation.extend(list_value)
        
        # BEBE
        value = fruit['description'].get('À partir de','')
        if value:
            list_bebe.append(value)
        
        # CONSERVATION
        value = fruit['description'].get("Conservation","")
        if value:
            list_conservation.append(value)
        
        # APPORT ENERGIE
        value = fruit['description'].get("Apport", "")
        if value:
            list_apport.append(int(re.findall(r"^\d+",value)[0]))
    
    if fruit['composition']:
        value = fruit['composition'].get("Eau", "")
        if value:
            list_eau.append(float(re.findall(r"^[\d.]+",value.replace(',','.'))[0]))

list_cultivation = sorted(list(set(list_cultivation)))
list_bebe = sorted(set(list_bebe), key= lambda x : int(x.split()[0]))

with st.sidebar:
    st.header("FILTRE")
    ##################
    # PAYS PRODUCTEUR
    ##################
    activation_cultivation = st.toggle("Par pays producteur")
    if activation_cultivation:
        option_pays = st.multiselect(
            "Quelles pays souhaitez-vous sélectionner ?", 
            list_cultivation,
            label_visibility = "visible",
        
        )
        if option_pays:
            # FILTRE SELON LE PAYS PRODUCTEUR
            list_fruit = [fruit for fruit in list_fruit if any([pays in fruit['description'].get("Cultivé", "") for pays in option_pays])]

    #######################
    # A PARTIR DE L'AGE
    #######################
    # activation_age = st.toggle("Par âge (pour bébé)")
    # if activation_age:
    options_age = st.pills("Age conseillé pour bébé", list_bebe, selection_mode="single")
    if options_age:
        list_fruit = [fruit for fruit in list_fruit if options_age == fruit['description'].get("À partir de", "")]#[fruit for fruit in list_fruit if any([age in fruit['description'].get("À partir de", "") for age in options_age])]
        
    
    ########################
    # TEMPS DE CONSERVATION
    ########################
    # Recherche des éléments (jour, semaine et mois dans chaque fruit)
    list_delais = set([re.findall(r"jour|mois|semaine",conservation)[0].title() for conservation in list_conservation if re.findall(r"jour|mois|semaine",conservation)])
    # trie par ordre : jour, semaine, mois
    list_delais = sorted(list_delais, key = lambda x : dict_tri_jour_semaine_mois[x])
    
    option_conservation = st.segmented_control("Délais de conservation", 
                                   list_delais , selection_mode="single")
    if option_conservation in ["Semaine", "Mois"]:
        list_fruit = [fruit for fruit in list_fruit if option_conservation.lower() in fruit['description'].get("Conservation", "")]
    elif option_conservation == "Jour":
        list_fruit = [fruit for fruit in list_fruit if not any([option.lower() in fruit['description'].get("Conservation", "") for option in ["Semaine", "Mois"]])]
    
    
    ########################
    # NOMBRE DE KCAL
    ########################
    st.subheader('Nombres de calories')
    minimum_apport_list_fruit, maximum_apport_list_fruit = min(list_apport), max(list_apport)
    minimum, maximum = st.slider("Sélectionnez l'intervalle", 
                                 minimum_apport_list_fruit, 
                                 maximum_apport_list_fruit,
                                 (minimum_apport_list_fruit, maximum_apport_list_fruit))
    
    # CETTE CONDITION PERMET DE GARDER LES FRUITS QUI N'ONT PAS D'INFORMATION SUR LEUR KCAL
    if minimum_apport_list_fruit == minimum and maximum_apport_list_fruit == maximum:
        pass
    else:
        list_fruit = [fruit for fruit in list_fruit if (fruit['description'].get("Apport", "") and minimum <= int( re.findall(r"^\d+",fruit['description'].get("Apport"))[0]) <= maximum)]
    # TRI SELON CROISSANT/DECROISSANT
    trie_apport = st.segmented_control("",["Croissant", "Décroissant"],selection_mode="single", label_visibility="collapsed", key = "tri_calorie")
    # FLAG PERMETTANT DE NE PAS FAIRE FONCTIONNER LE TRI EAU
    if trie_apport:
        list_fruit = [fruit for fruit in list_fruit if re.findall(r"^\d+",fruit['description'].get("Apport",""))]
        list_fruit = sorted(list_fruit, key = lambda x : int(re.findall(r"^\d+",x['description'].get("Apport"))[0]))
        if trie_apport == "Décroissant":
            list_fruit = list_fruit[::-1]
        tri_flag = True
    else :
        tri_flag = False
  
    ########################
    # QUANTITE D'EAU
    ########################
    minimum_eau_list_fruit, maximum_eau_list_fruit = min(list_eau), max(list_eau)
    minimum, maximum = st.slider("Sélectionnez l'intervalle", 
                                 minimum_eau_list_fruit, 
                                 maximum_eau_list_fruit,
                                 (minimum_eau_list_fruit, maximum_eau_list_fruit))
    
    # CETTE CONDITION PERMET DE GARDER LES FRUITS QUI N'ONT PAS D'INFORMATION SUR LEUR KCAL
    if minimum_eau_list_fruit == minimum and maximum_eau_list_fruit == maximum:
        pass
    else:
        list_fruit = [fruit for fruit in list_fruit if (fruit.get('composition', "") and fruit['composition'].get("Eau", "") and minimum <= float( re.findall(r"\A[\d.]+",fruit['composition'].get("Eau", "").replace(",","."))[0]) <= maximum)]
    
    
    # TRI SELON CROISSANT/DECROISSANT
    if tri_flag:
        pass
    else:
        trie_eau = st.segmented_control("",["Croissant", "Décroissant"],selection_mode="single", label_visibility="collapsed", key="tri_eau")
        # Croisant
        if trie_eau:
            list_fruit = [fruit for fruit in list_fruit if (fruit.get('composition', "") and re.findall(r"^[\d.]+",fruit['description'].get("Apport","")))]
            list_fruit = sorted(list_fruit, key = lambda x : float(re.findall(r"^[\d.]+",x['composition'].get("Eau", "").replace(",","."))[0]))
            if trie_eau == "Décroissant":
                list_fruit = list_fruit[::-1]
            
            
    
#############################

# MAIN (SUITE)

#############################
# Création de deux colonnes, Une pour les fruits et l'autre pour les informations
col1, col2 = st.columns([2, 1])

if list_fruit:
    with col1 :
        with st.container():
            index_fruit = image_select("Fruits Exotiques", 
                            images = [i['lien_image'] for i in list_fruit],
                            captions = [i['nom'] for i in list_fruit],
                            return_value="index", use_container_width=False)
    # st.write(list_fruit[index_fruit])

    fruit = list_fruit[index_fruit]
    with st.container():
        with col2:
            st.header(fruit['nom'])
            for key, value in fruit['description'].items():
                st.write(f"{dict_emoji.get(key.replace("A", "À"),"")} **{key}** : {value}")
            composition = fruit.get("composition", None)
            if composition:
                st.markdown("___")
                st.subheader("Composition (*pour 100g*) :")
                for key, value in composition.items():
                    st.write(f"{dict_emoji.get(key.replace("A", "À"),"")} **{key}** : {value}")
else : st.error('Aucun fruits ne correspond à ces filtres', icon="🚨")