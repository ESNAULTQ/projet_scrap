import requests
from bs4 import BeautifulSoup
import csv

def scrap_page(url):
    # Récupérer le contenu HTML de la page
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération de la page {url}")
        return []

    # Utiliser BeautifulSoup pour parser le contenu HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver les éléments correspondant aux offres d'emploi
    offres_emploi = soup.find_all('a', class_="node-offre_emploi--teaser-title")
    localisation = soup.find_all('span', class_="node-offre_emploi--teaser-city")
    date = soup.find_all('span', class_="node-offre_emploi--teaser-date")
    contrat = soup.find_all('span', class_="tag-rh tag-typeContract")
    secteur = soup.find_all('span', class_="tag-rh tag-filiere")
    id_offre = soup.find_all('li', class_="node node--teaser node-offre_emploi node-offre_emploi-teaser node-offre_emploi--teaser swiper-slide")

    # Créer une liste pour stocker les détails des offres d'emploi
    offres_emploi_details = []

    # Parcourir les offres d'emploi et extraire leurs détails
    for i in range(len(offres_emploi)):
        offre_details = {
            "Titre": offres_emploi[i].text.strip(),
            "Localisation": localisation[i].text.strip(),
            "Date": date[i].text.strip(),
            "Contrat": contrat[i].text.strip(),
            "Secteur": secteur[i].text.strip(),
            "ID": id_offre[i].text.strip()
        }
        offres_emploi_details.append(offre_details)

    return offres_emploi_details

# Stocker les données dans un dictionnaire
all_offers = {}

# Afficher les pages 1 à 5:
for page in range(0, 5):
    url_page = f'https://www.enedis.fr/emploi?recherche=Data&sort_by=search_api_relevance&page={page}'
    offres_page = scrap_page(url_page)
    all_offers[f"Page_{page}"] = offres_page

# Écrire les données dans un fichier CSV
with open('offres_emploi.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["Titre", "Localisation", "Date", "Contrat", "Secteur", "ID"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for page, offres in all_offers.items():
        for offre in offres:
            writer.writerow(offre)

​
​
