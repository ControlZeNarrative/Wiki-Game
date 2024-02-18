import requests
import wikipedia
from bs4 import BeautifulSoup
import random

def get_wikipedia_link(query):
    try:
        page = wikipedia.page(query)
        return page.url
    except wikipedia.exceptions.PageError:
        return None

def scrapeWikiArticle(url, n):
    if n >= 10:
        return
	
    try:
        response = requests.get(url=url)
    except Exception as e:
        print("Request failed: " + str(e))
        return
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")
    print(title.text)

    allLinks = soup.find(id="bodyContent").find_all("a")
    random.shuffle(allLinks)
    linkToScrape = 0

    for link in allLinks:
        if 'href' not in link.attrs:
            continue
		# Make sure this is only a wiki link
        if link['href'].find("/wiki/") == -1: 
            continue

		# Use this link to scrape
        linkToScrape = link
        break

    scrapeWikiArticle("https://en.wikipedia.org" + linkToScrape['href'], n + 1)


search_query = input("Enter your search query: ")
link = get_wikipedia_link(search_query)
if (link):
      scrapeWikiArticle(link, 0)
      print("--------------------------------------------\nDone!")
else:
      print("Your input's wikipedia's page was not found")
