from bs4 import BeautifulSoup
from dotenv import load_dotenv
import discord
import requests

import os
import re

load_dotenv()
client = discord.Client()
embed = discord.Embed()
PREFIX = '$'
URL = f"https://1lib.in"
HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"}

# Function to call for fetching data using the given argument
def get_content(keyword):
    search = f"{URL}/s/{keyword}"
    result = requests.get(search, HEADER).text
    doc = BeautifulSoup(result, "html.parser")

    container = doc.find("h3", {"itemprop": "name"})
    code = container.a["href"]
    name = container.a.string
    # path = f"**{name}:** {URL}{code}"

    embed.description = f"[{name}]({URL}{code})"
    # Need changes for direct download link
    # download = f"{URL}/dl/{code[6:]}?openInBrowser"
    
    return embed
    

if __name__ == "__main__":
    # Event when bot is ready
    @client.event
    async def on_ready():
        print(f"{client.user} is ready!")
        status = discord.Game(name="$get <book-name>")
        await client.change_presence(activity=status)


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        # Split command and argument from the message
        if message.content.startswith(PREFIX):
            msg = message.content.strip()[len(PREFIX):]
            cmd, *args = re.sub(re.compile(r'\s+'), ' ', msg).split(' ')

            match cmd:
                case "get":
                    name = ""
                    for words in args:
                        name += words + " "
                    name.strip()

                    link = get_content(name)
                    await message.reply(embed = link)


    client.run(os.getenv("TOKEN"))

