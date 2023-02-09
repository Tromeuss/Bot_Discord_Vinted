from fonction import *
import time
import asyncio

def main():
    #A CHANGER ------------------
    COOLDOWN = 60*5  #en seconde
    #----------------------------

    liste_id = []
    while True:
        with open ("config.json",'r') as file:
            texte = json.load(file)

        params={}
        count=0
        for i in texte["suburl"]:
            params2={}
            params2["BOT"] = i
            params2["URL"] = texte["suburl"][i]["url"] 
            params[count] = params2
            count=count+1


        #Actualise tous les salons
        for loop in range(len(params)):

            items = search(params[loop]["URL"])
            for element in items:
                if isNew(items[element],COOLDOWN) and items[element]["id"] not in liste_id:
                    discord_send(items[element],params[loop]["BOT"],params[loop]["URL"])
                    time.sleep(3)
                    liste_id.append(items[element]["id"])
            if texte["stop"] == "True":
                break
            print("SALON NUMERO ", loop, "ACTUALISER")
            time.sleep(2)
        time.sleep(2)
