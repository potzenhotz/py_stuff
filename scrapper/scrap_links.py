from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

req = Request("http://www.anuga.de/aussteller-und-produkte/ausstellerverzeichnis/ausstellerverzeichnis-9.php?fw_goto=aussteller/index&&tab=2&stichwort=&suchart=&suchort=&GRUPPIERUNG[00044]=&GRUPPIERUNG[00045]=&GRUPPIERUNG[00046]=&GRUPPIERUNG[00047]=")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

print(links)
 
