import requests
import pandas as pd
from bs4 import BeautifulSoup, Tag
import time

###
dict_final_avant_json = dict()

mois_de_l_anne = ["janvier" ,"fevrier", "mars", "avril" ,"mai", "juin", "juillet", "aout", "septembre", "octobre","novembre", "decembre"]

# Declaration des éléments
memory_fruit_legume = dict()
dict_fruits = dict()
dict_legumes = dict()

for mois in mois_de_l_anne:
    print(mois)
    url = f"https://www.lesfruitsetlegumesfrais.com/calendrier-fruits-legumes/{mois}"
    navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
    ###
    res = requests.get(url, headers={'User-Agent': navigator})

    # forcer le décodage en UTF-8 depuis les bytes bruts
    html = res.content.decode("utf-8", errors="ignore")

    soup = BeautifulSoup(html, "html5lib")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # Creation des listes fruits et légumes
    list_fruits = list()
    list_legumes = list()
        

    # Liste des des differents html par fruits/légumes
    fruits = soup.find_all("div", class_="calendar__item")

    for fruit in fruits:
        if not isinstance(fruit, Tag):
            continue
        
        # Recuperation du nom du fruit et du lien de l'image
        img_tag = fruit.find("img") 
        image = img_tag["src"]  if img_tag else None # type: ignore
        
        nom_tag = fruit.find("div", class_="card__title")
        nom = nom_tag.get_text(strip=True) if nom_tag else None
        # print(nom, image)
        
        # Catégories légume ou fruit
        try:
            categorie = [i for i in fruit.get('class') if i.startswith('type_product')][0].replace('type_product-','') # type: ignore
            # print(categorie)
        except:
            category = None
        
        if not nom:
            continue

        # Recuperation du lien de la fiche produit du fruit
        site_fruit = fruit.find("div", class_="card__actions").find("a", class_="dl-notice")['href'] # type: ignore
        
        if nom not in memory_fruit_legume.keys():
            # traverser site du fruit:
            if site_fruit:
                time.sleep(0.5)
                res_fruit = requests.get(site_fruit, headers={'User-Agent': navigator}) # type: ignore

                # forcer le décodage en UTF-8 depuis les bytes bruts
                html_fruit = res_fruit.content.decode("utf-8", errors="ignore")

                soup_fruit = BeautifulSoup(html_fruit, "html5lib")
                
                
                ##########################
                
                # Partie info pratique
                
                ##########################   
                # print("\nPartie informations") 
                description = dict()
                try:
                    info_pratiques = soup_fruit.find_all("div", class_="nutriscore__icons")
                    for info_pratique in info_pratiques:
                        titre = info_pratique.find("div", class_="icons").get_text(strip=True) # type: ignore
                        information = info_pratique.find("span", class_="texts").get_text(strip=True) # type: ignore
                        description[titre] = information
                        # print(titre, ':', information)
                except:
                    # print(None)
                    description = None
            
                
                ##########################
                
                # Partie Composition
                
                ##########################
                # print("\nPartie Compositions") 
                composition_dict = dict()
                try:
                    compositions = soup_fruit.find("div", class_="product__composition").find("tbody").find_all('tr') # type: ignore
                    for composition in compositions:
                        titre_composition = composition.find('td').text # type: ignore
                        information_composition = composition.find('th').text # type: ignore
                        composition_dict[titre_composition] = information_composition
                        # print(titre_composition, ':', information_composition)
                except:
                    # print(None)
                    composition_dict = None
                    
                # Uniformisation
                dict_fruit_legume = {
                    "nom" : nom,
                    "lien_image" : image,
                    "description" : description,
                    "composition" : composition_dict
                }

            if categorie == "fruits":
                list_fruits.append(dict_fruit_legume) 
            else:
                list_legumes.append(dict_fruit_legume)
            memory_fruit_legume[nom] = dict_fruit_legume
                
        else:
            if categorie == "fruits":
                list_fruits.append(memory_fruit_legume[nom]) 
            else:
                list_legumes.append(memory_fruit_legume[nom])
                
    print("fruits" ,":", len(list_fruits))  
    print("legumes" ,":", len(list_legumes))  

    dict_fruits[mois] = list_fruits
    dict_legumes[mois] = list_legumes
    
    dict_final_avant_json[mois] = {
    "fruits" : list_fruits,
    "legumes" : list_legumes
    }

dict_main = {
    "fruits" : dict_fruits,
    "legumes" : dict_legumes
}
    
#################################

# Transformation en JSON

#################################
import json
final_json = json.dumps(dict_final_avant_json, indent=6, ensure_ascii=False, sort_keys=False)
with open("data/seasons_fruits_legs.json", 'w', encoding='utf-8') as f:
    f.write(final_json)