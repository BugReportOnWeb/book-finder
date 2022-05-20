<h1 id="header" align="center">
    Book Finder
    <div id="badge">
        <img id="code-size" src="https://img.shields.io/github/languages/code-size/BugReportOnWeb/book-finder" />
        <img id="last-commit" src="https://img.shields.io/github/last-commit/BugReportOnWeb/book-finder" />
    </div>
</h1>

Discord bot made using discord.py to fetch books from [1lib.in](https://1lib.in)
```
SYNOPSIS
    $get <book-name>        # Returns the possible book related to the given book name.
    $find <book-genre>      # Returns the top 5 book in the specified genre.
```

## Dependencies
* [discord.py](https://pypi.org/project/discord.py/) -> A Python Wrapper for Discord API.
```
python3 -m pip install -U discord.py
```
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) -> Screen-scraping library.
```
python3 -m pip install -U beautifulsoup4
```
* [python-dotenv](https://pypi.org/project/python-dotenv/) -> Read key-value pairs from a .env file and set them as environment variables.
```
python3 -m pip install -U python-dotenv
```
* [requests](https://pypi.org/project/requests/) -> Python HTTP for Humans.
```
python3 -m pip install -U requests
```
