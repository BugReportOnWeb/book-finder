#!/usr/bin/env python3

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import discord
import requests

import os
import re

load_dotenv()
client = discord.Client()
embed = discord.Embed(color=15105570)

PREFIX = '$'
URL = f"https://1lib.in"
HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"}

# Functions for fetching a group of books from the given genre
def find(keyword):
    global no_output
    no_output = False

    embed.title = embed.description = ''
    embed.set_thumbnail(url='')

    search = f"{URL}/s/{keyword}"
    result = requests.get(search, HEADER).text
    doc = BeautifulSoup(result, "html.parser")

    cards = doc.find_all("div", {"class": "resItemBox resItemBoxBooks exactMatch"})

    if len(cards) >= 5:
        output_range = 5
    elif len(cards) == 0:
        embed.description += f"On your request nothing has been found :("
        no_output = True
        return embed
    else:
        output_range = len(cards)

    for item in range(output_range):
        container = cards[item].find("h3", {"itemprop": "name"})
        code = container.a["href"]
        name = container.a.string

        # Making a list of all the authors for the perticular book
        authors = cards[item].find("div", {"class": "authors"}).find_all("a")
        authors_string = ''

        for index in range(len(authors)):
            if index != len(authors) - 1:
                authors_string += f"{authors[index].string}, "
            else:
                authors_string += authors[index].string
        authors_string.strip()

        embed.description += f"⭐  [{name} ~ {authors_string}]({URL}{code})\n\n"
    
    return embed


# Function for fetching a specific book
def get(keyword):
    global no_output
    no_output = False

    embed.title = embed.description = embed.url = ''
    embed.set_thumbnail(url='')

    search = f"{URL}/s/{keyword}"
    result = requests.get(search, HEADER).text
    doc = BeautifulSoup(result, "html.parser")

    container = doc.find("h3", {"itemprop": "name"})

    try:
        code = container.a["href"]
    except AttributeError:
        embed.description += f"On your request nothing has been found :("
        no_output = True
        return embed

    name = container.a.string
    image = doc.find("img", {"class": "cover lazy"})["data-src"]

    authors = doc.find("div", {"class": "authors"}).find_all("a")
    authors_string = ''

    for index in range(len(authors)):
        if index != len(authors) - 1:
            authors_string += f"{authors[index].string}, "
        else:
            authors_string += authors[index].string
    authors_string.strip()

    embed.title += f"⭐  {name}"
    embed.description += authors_string
    embed.url = URL + code
    if image != "/img/cover-not-exists.png":
        embed.set_thumbnail(url=image)
    
    return embed   


if __name__ == "__main__":
    # Event when bot is ready
    @client.event
    async def on_ready():
        print(f"{client.user} is ready!")

        # Load image fromthe assets for the bot profile
        with open('./assets/image.jpg', 'rb') as image:
            await client.user.edit(avatar=image.read())

        status = discord.Game(name="$get <book-name> || $find <book-genre>")
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
                    # Combining all the argumens into a single string
                    book_name = ""
                    for words in args:
                        book_name += words + " "
                    book_name.strip()

                    output = get(book_name)
                    await message.reply(embed=output)

                    if no_output:
                        await message.add_reaction("😢")

                case "find":
                    if len(args) == 1:
                        output = find(args[0])
                        await message.reply(embed=output)
                    else:
                        embed.description = "Please specify a single genre (argument) with $find command"
                        embed.set_thumbnail(url='')
                        await message.reply(embed=embed)

                    if no_output:
                        await message.add_reaction("😢")

    client.run(os.getenv("TOKEN"))


    # random commentj
