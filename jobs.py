import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_job_offers(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Récupérer les données JSON de l'API
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        # Initialiser une liste pour stocker les données extraites
        job_data = []

        # Parcourir les éléments du contenu JSON
        for item in data['content']:
            # Extraire les données pertinentes
            job_id = item.get('id')  # Correction ici pour obtenir l'ID de l'emploi
            title = item.get('title')
            description_html = item.get('description')
            contract_type = item.get('contractTypes')[0] if item.get('contractTypes') else None
            publication_date = item.get('publicationDate')
            company_name = item.get('company').get('name') if item.get('company') else None  # Récupérer le nom de l'entreprise

            # Nettoyer la description HTML
            description_text = None
            if description_html:
                soup = BeautifulSoup(description_html, 'html.parser')
                description_text = soup.get_text(separator=' ')
                description_text = description_text.replace('\n', '')  # Supprimer les retours à la ligne

            # Récupérer les informations de localisation
            locations = item.get('locations')
            location_name = None
            if locations:
                location_name = locations[0].get('name')  # Prendre le nom de la première localisation

            # Stocker les données extraites dans un dictionnaire
            job_info = {
                'ID': job_id,
                'Title': title,
                'Description': description_text,
                'Contract Type': contract_type,
                'Publication Date': publication_date,
                'Company Name': company_name,  # Ajouter le nom de l'entreprise
                'Location': location_name,  # Ajouter le nom de la localisation
            }

            # Ajouter le dictionnaire à la liste
            job_data.append(job_info)

        # Créer un DataFrame à partir de la liste de dictionnaires
        df = pd.DataFrame(job_data)

        # Afficher le DataFrame
        return df
    else:
        print("Erreur lors de la requête HTTP:", response.status_code)

from datetime import datetime

def exportcsv(dataframe, index=True):
    date_str = datetime.today().strftime("%Y-%m-%d-%H%M")
    nom_fichier = f"rhone_alpes_jobs_{date_str}.csv"
    dataframe.to_csv(nom_fichier, index=index)
    return f"Exportation vers {nom_fichier} effectuée avec succès."

url = "https://nostalentsnosemplois.auvergnerhonealpes.fr/api/joboffers/search?serjobsearch=true&scoringVersion=SERJOBSEARCH&what=data&sorting=SCORING&page=3&limit=20&expandLocations=true&facet=cities&facet=date&facet=company&facet=industry&facet=contract&facet=job&facet=macroJob&facet=jobType&facet=content_language&facet=license&facet=degree&facet=experienceLevel"
df = scrape_job_offers(url)
exportcsv(df)
