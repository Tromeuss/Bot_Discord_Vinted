import discord
from discord.ext import commands
import os, json
import sys
import threading
from main_bot import *

stop_threads = False

with open("config.json","r+") as f:
    configs = json.load(f)

TOKEN = configs["token"]

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!",description="by ORAMI le goat",intents=intents)


@bot.event
async def on_ready():
    print("Ready!")

@bot.command()
async def sub(ctx, vintedurl):
    x = await ctx.channel.create_webhook(name="vinted-test")
    with open("config.json", 'w+') as configedit:
        configs["suburl"][str(x.url)] = {}
        configs["suburl"][str(x.url)]["url"] = str(vintedurl)
        configs["suburl"][str(x.url)]["salon"] = str(ctx.channel.name)
        json.dump(configs,configedit,indent=4)
    await ctx.send(f"{ctx.author.mention} - **✔️ Webhook ajouté avec le lien !**")
    return

@bot.command()
async def change_url(ctx, new_url):
    for weburl in configs["suburl"]:
        if configs["suburl"][weburl]["salon"] == ctx.channel.name:
            with open("config.json", 'w+') as configedit:
                configs["suburl"][str(weburl)]["url"] = str(new_url)
                json.dump(configs,configedit,indent=4)
    await ctx.send(f"{ctx.author.mention} - **✔️ Le lien du scrapping lié au salon {ctx.channel.name} a été modifié avec succès !**")
    return

@bot.command()
async def remove_sub(ctx):
    webhook = None
    for weburl in configs["suburl"]:
        if configs["suburl"][weburl]["salon"] == ctx.channel.name:
            webhook = weburl
            with open("config.json", 'w+') as configedit:
                del configs["suburl"][webhook]
                json.dump(configs,configedit,indent=4)
    await ctx.send(f"{ctx.author.mention} - **✔️ Le lien du scrapping lié au salon {ctx.channel.name} a été supprimé avec succès !**")
    return

@bot.command()
async def reinitialise(ctx):
    with open("config.json", 'w+') as configedit:
        del configs["suburl"]
        configs["suburl"] = {}
        json.dump(configs,configedit,indent=4)
    await ctx.send(f"{ctx.author.mention} - **✔️ Tout a été réinitialiser !**")
    return

@bot.command()
async def info(ctx):
    with open("config.json","r+") as f:
        configs = json.load(f)
    await ctx.send(f"{configs}")

@bot.command()
async def run(ctx):
    global t1
    with open("config.json", 'w+') as configedit:
        configs["stop"] = "False"
        json.dump(configs,configedit,indent=4)
    t1 = threading.Thread(target=main)
    # démarrer le thread t1
    t1.start()
    await ctx.send("**C'est partit. ATTENTION // Tant que vous ne l'avez pas arrété avec la fonction !stop , ne réexécutez pas cette commande! **")

@bot.command()
async def stop(ctx):
    with open("config.json", 'w+') as configedit:
        configs["stop"] = "True"
        json.dump(configs,configedit,indent=4)
    await ctx.send("**C'est finit. ATTENTION // Tant que vous ne l'avez pas relancé avec !run , ne réexécutez pas cette commande!**")
    

@bot.command()
async def liste_commande(ctx):
    await ctx.send("**!sub <url> -> Pour relier le salon actuel avec un lien vinted**")
    await ctx.send("**!change_url <url> -> Pour relier le salon actuel avec un nouveau lien vinted**")
    await ctx.send("**!remove_sub  -> Pour supprimer la paire salon/url**")
    await ctx.send("**!reinitialise -> Remet tout a zero**")
    await ctx.send("**!info -> Obtiens les données json**")
    await ctx.send("**!run  -> Une fois que tout est configuré.NE REEXECUTEZ PAS 2 FOIS D'AFFILER CETTE COMMANDE**")
    await ctx.send("**!stop  -> Les annonces cessent d'étre envoyé.Vous pouvez le relancer en relancant !run **")

bot.run(TOKEN)
