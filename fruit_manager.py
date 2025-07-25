import json

def ouvrir_prix(path="data/prix.json"):
    with open(path, 'r', encoding='utf-8') as fichier:
        prix = json.load(fichier)
    return prix

def ouvrir_inventaire(path = "data/inventaire.json"):
    with open(path, 'r', encoding='utf-8') as fichier:
        inventaire = json.load(fichier)
    return inventaire

    
def ecrire_inventaire(inventaire, path="data/inventaire.json"):
    with open(path, 'w', encoding='utf-8') as fichier:
        json.dump(inventaire, fichier, ensure_ascii=False, indent=4)

def ouvrir_tresorerie(path="data/tresorerie.txt"):
    with open(path, 'r', encoding='utf-8') as fichier:
        tresorerie = json.load(fichier)
    return tresorerie

def ecrire_tresorerie(tresorerie,path="data/tresorerie.txt"):
    with open(path, 'w', encoding='utf-8') as fichier:
        json.dump(tresorerie, fichier, ensure_ascii=False, indent = 4)

def afficher_tresorerie(tresorerie, path = "data/trésorerie.txt"):
    print(f"\n💰 Trésorerie actuelle : {tresorerie:.2f} $")

def afficher_inventaire(inventaire:dict[str, int]):
    print("Inventaire actuel de plantation :")
    for fruit, quantite in inventaire.items():
        print(f"- {fruit.capitalize()} : {quantite} unités" ) 
        
        
        
def recolter(inventaire:dict[str, int], fruit:str, quantite:int):
    inventaire[fruit] = inventaire.get(fruit, 0) + quantite
    print(f"\n✅ Récolté {quantite} {fruit} supplémentaires !")
    


def vendre(inventaire, fruit, quantite, tresorerie, prix:dict):
    if inventaire.get(fruit, 0) >= quantite:
        inventaire[fruit] -= quantite 
        tresorerie += 1 * quantite* prix.get(fruit)
        print(f"\n💰 Vendu {quantite} {fruit} !")  
    else:
        print(f"\n❌ Pas assez de {fruit} pour vendre {quantite} {fruit} unités.")
    return (inventaire, tresorerie)

        
if __name__ == "__main__":
    inventaire = ouvrir_inventaire()
    tresorerie = ouvrir_tresorerie()
    prix = ouvrir_prix()
    afficher_tresorerie(tresorerie)
    afficher_inventaire(inventaire)
    
    recolter(inventaire, "bananes", 10)
    inventaire, tresorerie = vendre(inventaire, "bananes", 5, tresorerie, prix)
    
    ecrire_inventaire(inventaire)
    ecrire_tresorerie(tresorerie)