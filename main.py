# skeleton of this code provided by prof

# This library lets you get webpages.
import requests

# Beautifulsoup, which you already know.
from bs4 import BeautifulSoup

# Here's a Category page for Simple English Wikipedia
URL = "https://simple.wikipedia.org/wiki/Category:Felines"

# Get that page.
page = requests.get(URL)

# Now parse the html.
soup = BeautifulSoup(page.content, "html.parser")

# List for storing the links to pages we want to get.
cat_pages = []

# Find the heading associated with "Pages in category"
# Depending on the Category page you are looking at.
# you might need to change the text you want to match.
for h2 in soup.find_all("h2"):
    if "Pages in category" in h2.text:

        # Find all subsequent a href tags.
        # This is 46 because that's how many I found on this
        # particular page. You will have to change that to
        # work with anothe rpage.
        for a in h2.find_all_next("a", href=True, limit=46):
            if "wiki" in a["href"]:
                cat_pages.append(a["href"])

# For each URL you got out of the Category page...
for c in cat_pages:

    # You need to add the rest of the URL to the beginning.
    URL = "https://simple.wikipedia.org/" + c

    # Go get it and parse the html.
    page = requests.get(URL)
    newsoup = BeautifulSoup(page.content, "html.parser")

    # Print out all the text.
    for info in newsoup.find_all("p"):
        print(info.get_text())
