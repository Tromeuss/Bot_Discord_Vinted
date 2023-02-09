from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
import chromedriver_autoinstaller
from selenium import webdriver
import time
import requests
import json
import time
from discordwebhook import Discord
from requests import Session, post
import datetime
import mechanize
import re

def formated():
  with open("output.json", 'r') as f:
    try:
      data = json.load(f)
    except json.decoder.JSONDecodeError as e:
      # Position de l'erreur dans le fichier
      pos = e.pos
      f.seek(0)
      # Liste des lignes du fichier
      lines = f.readlines()
      new_lines = []
      # On parcourt les lignes du fichier
      for line in lines:
        if '"' in line:
          # On calcule la position de l'erreur
          line_pos = sum(len(l) for l in new_lines)
          if line_pos <= pos < line_pos + len(line):
            # On remplace le caractère à la position de l'erreur
            start, end = line[:pos-line_pos-1], line[pos-line_pos:]
            line = start + 'E' + end
            # On effectue les autres remplacements nécessaires
            new_lines.append(line)
            # On sauvegarde les lignes formatées dans un nouveau fichier
            with open('output.json', 'w') as f2:
              f2.writelines(line)

def formated2():
  with open("output.json", 'r') as f:
    try:
      data = json.load(f)
    except json.decoder.JSONDecodeError as e:
      # Position de l'erreur dans le fichier
      pos = e.pos
      f.seek(0)
      # Liste des lignes du fichier
      lines = f.readlines()
      new_lines = []
      # On parcourt les lignes du fichier
      for line in lines:
        if '"' in line:
          # On calcule la position de l'erreur
          line_pos = sum(len(l) for l in new_lines)
          if line_pos <= pos < line_pos + len(line):
            # On remplace le caractère à la position de l'erreur
            start, end = line[:pos-line_pos-2], line[pos-line_pos-1:]
            line = start + 'E' + end
            # On effectue les autres remplacements nécessaires
            new_lines.append(line)
            # On sauvegarde les lignes formatées dans un nouveau fichier
            with open('output.json', 'w') as f2:
              f2.writelines(line)

def search(url):
    """titre,price,url,photo,marque,devise,taille,date,hauteur,hauteur_photo,id"""
    br=mechanize.Browser()
    try:
        br.open(url)
        mess = str(br.response().read())
    except:
        print("Maximum de requete, on va attendre un peu")
        time.sleep(10)
        mess = "NULLE"
    with open("data.html", "w", encoding="utf-8") as f:
        f.write(mess)
    br.close()

    #Découper le code source pour avoir que la partie json et l'écris dans output.json

    # Mots début et fin à rechercher
    start_word = '{"catalogItems"'
    end_word = '"endReached"'
    ajout = ':false}}'
    # Charger le contenu du fichier html
    with open("data.html", "r", encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Rechercher la portion entre les mots début et fin
    match = re.search(f"{start_word}(.*?){end_word}", content, re.DOTALL)

    # Vérifier si la portion a été trouvée
    if match:
        # Extraire la portion trouvée et la stocker dans une variable
        result = match.group(1)

        # Enregistrer le résultat dans un fichier json
        with open("output.json", "w", encoding='utf-8', errors='ignore') as file:
            mess = f"{start_word}{result}{end_word}{ajout}"
            mess = mess.replace("\\",'')
            file.write(mess)
    else:
        print('ERROR NON FATALE // ON A PAS TROUVER LA PORTION , SOUCIS AVEC LE FICHIER DATA.HTML, ON PASSE AU SALON SUIVANT')

    condition = False
    while condition == False:
        #ENLEVE LE PREMIER GUILLEMET
        with open("output.json", "r", encoding='utf-8', errors='ignore') as json_file:
            try:
                data_dict=json.load(json_file)
                break
            except json.decoder.JSONDecodeError as e:
                formated()
        #ENLEVE LE DEUXIEME GUILLEMET
        with open("output.json", "r", encoding='utf-8', errors='ignore') as json_file:
            try:
                data_dict=json.load(json_file)
                break
            except json.decoder.JSONDecodeError as e:
                formated2()
        #RETESTE
        with open("output.json", "r", encoding='utf-8', errors='ignore') as json_file:
            try:
                data_dict=json.load(json_file)
                break
            except:
                print("ON A ENLEVER 2 GUILLEMETS MAIS çA SUFFIT PAS, ON RECOMMENCE")

    
    final_dico={}
    for loop in range(len(data_dict['catalogItems']['ids'])):  
        dico={}
        try:
            dico["titre"] = data_dict['catalogItems']["byId"][str(data_dict['catalogItems']["ids"][loop])]["title"]
        except:
            dico["titre"] = "ERROR"
        try:
            dico["price"] = data_dict['catalogItems']["byId"][str(data_dict['catalogItems']["ids"][loop])]["price"]
        except:
            dico["price"] = "ERROR"
        try:
            dico["url"] = data_dict['catalogItems']["byId"][str(data_dict['catalogItems']["ids"][loop])]["url"]
        except:
            dico["url"] = "ERROR"
        try:
            dico["photo"] = data_dict['catalogItems']["byId"][str(data_dict['catalogItems']["ids"][loop])]["photo"]["url"]
        except:
            dico["photo"] = "https://i1.sndcdn.com/artworks-3Yrzcz1fRIAjvF3p-B24y4g-t500x500.jpg"
        try:
            dico["marque"] = data_dict['catalogItems']["byId"][str(data_dict['catalogItems']["ids"][loop])]["brand_title"]
        except:
            dico["marque"] = "ERROR"
        try:
            dico["devise"] = data_dict['catalogItems']["byId"][str(data_dict['catalogItems']["ids"][loop])]["currency"]
        except:
            dico["devise"] = "ERROR"
        try:
            dico["taille"] = data_dict['catalogItems']["byId"][str(data_dict['catalogItems']["ids"][loop])]["size_title"]
        except:
            dico["taille"] = "ERROR"
        try:
            dico["date"] = data_dict['catalogItems']["byId"][str(data_dict['catalogItems']["ids"][loop])]["photo"]["high_resolution"]["timestamp"]
        except:
            dico["date"] = 0
            print("AAAAAAAAAAAAAAA")
        try:
            dico["auteur"] = data_dict['catalogItems']["byId"][str(data_dict['catalogItems']["ids"][loop])]["user"]["login"]
        except:
            dico["auteur"] = "ERROR"
        try:
            dico["auteur_photo"] = data_dict['catalogItems']["byId"][str(data_dict['catalogItems']["ids"][loop])]["user"]["photo"]["url"]
        except:
            dico["auteur_photo"] = "https://i1.sndcdn.com/artworks-3Yrzcz1fRIAjvF3p-B24y4g-t500x500.jpg"
        try:
            dico["id"] = str(data_dict['catalogItems']["ids"][loop])
        except:
            dico["id"] = "0"

        final_dico[loop] = dico
    return final_dico

def isNew(objet,temps):
    return (time.time() - int(objet["date"])) < temps

def discord_send(item,webhook,recherche):
    start_word = 'search_text='
    end_word = '&'
    match = re.search(f"{start_word}(.*?){end_word}", recherche, re.DOTALL)

    # Vérifier si la portion a été trouvée
    if match:
        # Extraire la portion trouvée et la stocker dans une variable
        result = match.group(1)
    else:
        result = "ERROR"
    discord = Discord(url=webhook)
    title = item["titre"] 
    price = item["price"]
    devise = item["devise"]
    url = item["url"]
    photo = item["photo"]
    marque = item["marque"]
    date = item["date"]
    auteur = item["auteur"]
    auteur_photo = item["auteur_photo"]
    taille = item["taille"]
    print("SEND")
    discord.post(
        username="VINTED TOMA",
        avatar_url= "https://static.vecteezy.com/ti/vecteur-libre/p3/4437510-text-reading-bot-glyph-icon-screen-reader-application-virtual-assistant-robot-with-book-software-app-speech-synthesizer-silhouette-symbol-negative-space-vector-isolated-illustration-vectoriel.jpg",
        embeds=[{
            "title": f"{title}",
            "fields": [
                {"name": "Prix","value": f"{price} {devise}","inline": True},
                {"name": "Marque","value": f"{marque}","inline": True},
                {"name": "Taille","value": f"{taille}","inline": True},
                {"name": "Vendeur","value": f"{auteur}","inline": True},
                {"name":"Recherche associé","value":f"{result}"}
            ],
            "image": {
                "url": f"{photo}"
            },
            "thumbnail": {"url": f"{auteur_photo}","name":"vendeur","value":f'{auteur}'},
            "footer": {
                "text": f"{datetime.datetime.fromtimestamp(date).isoformat()}",
            },
            "author": {
                "name": "VOIR LE PRODUIT",
                "url": f"{url}",
            "icon_url": "https://news.chastin.com/wp-content/uploads/2021/05/vinted.jpg",
            }
        }],
    )

