import urllib.request as urllib
import bs4
import html2text

url ='https://de.finance.yahoo.com/q/ao?s=GILD'

beautiful = urllib.urlopen(url).read()
soup = bs4.BeautifulSoup(beautiful, 'lxml')

'''
with open('out.txt', 'w') as f:
    f.write(soup.prettify())
'''

txt = html2text.html2text(soup.get_text())
str1 = "Empfehlung (diese Woche):";
len_val = 3
str1_and_value = (txt[txt.find(str1):txt.find(str1) + len(str1) + len_val]
str1_value = txt[txt.find(str1)+ len(str1):txt.find(str1) + len(str1) + len_val]

