import pandas as pd
from bs4 import BeautifulSoup
import re

f = open('AS_publications2019-21.txt', 'r')

i=0
j=0
k=0
l=0
m=0
n=0
titles = []
authors_list = []
biblio_codes = []
keywords = []
abstracts = []
urls = []

a_re = "[A-Z][a-zA-Z]+\s?[a-zA-Z0-9.]+\s?[+-]?\s?[0-9]?[0-9]+"
b_re = "[M][0-9]?[0-9]+"
c_re = "[0-9][A-Z][+]?\s?[0-9]+[+-.]?[0-9]+"
d_re = "[A-Z][0-9]+\s?[A-Z][a-z]+"
e_re = "[A-Z][0-9]+\s?[A-Z][a-z]+"

source_names = []

source_set = None

a=False
b=False
c=False

for line in f.readlines():
    if line.__contains__("Title:"):
        title = line.split("Title:")[-1].strip()
        print(title)
        titles.append(title)
        i+=1

        x = re.findall(a_re, title)
        source_set = set(x)
        y = re.findall(b_re, title)
        source_set.update(set(y))
        z = re.findall(c_re, title)
        source_set.update(set(z))
        w = re.findall(d_re, title)
        source_set.update(set(w))
        v = re.findall(e_re, title)
        source_set.update(set(v))

        a=True

    elif line.__contains__("Authors:"):
        authors = line.split("Authors:")[-1].strip()
        print(authors)
        authors_list.append(authors)
        j+=1
    
    elif line.__contains__("Bibliographic Code:"):
        code = line.split("Bibliographic Code:")[-1].strip()
        print(code)
        biblio_codes.append(code)
        k+=1
    
    elif line.__contains__("Keywords:"):        
        keyword = line.split("Keywords:")[-1].strip()
        print(keyword)
        l+=1
        keywords.append(keyword)

        x = re.findall(a_re, keyword)
        source_set.update(set(x))
        y = re.findall(b_re, keyword)
        source_set.update(set(y))
        z = re.findall(c_re, keyword)
        source_set.update(set(z))
        w = re.findall(d_re, keyword)
        source_set.update(set(w))
        v = re.findall(e_re, keyword)
        source_set.update(set(v))

        c=True
    
    elif line.__contains__("Abstract:"):
        abstract = line.split("Abstract:")[-1].strip()
        print(abstract)
        abstracts.append(abstract)
        m+=1

        x = re.findall(a_re, abstract)
        source_set.update(set(x))
        y = re.findall(b_re, abstract)
        source_set.update(set(y))
        z = re.findall(c_re, abstract)
        source_set.update(set(z))
        w = re.findall(d_re, abstract)
        source_set.update(set(w))
        v = re.findall(e_re, abstract)
        source_set.update(set(v))

        b=True

    elif line.__contains__("URL:"):
        url_line = BeautifulSoup(line)
        for tag in url_line.findAll('a', href=True):
            url = tag['href']
        print(url)
        urls.append(url)
        n+=1
    
    elif a and b and c:
        source_names.append(list(source_set))
        b=False
        c=False



print(i)
print(j)
print(k)
print(l)
print(m)
print(n)
print(len(source_names))

df = pd.DataFrame({'Title':titles, 'URL':urls, 'Sources':source_names, 'Authors':authors_list, 'Keywords':keywords, 'Abstract':abstracts})

df.to_csv('publications.csv')
