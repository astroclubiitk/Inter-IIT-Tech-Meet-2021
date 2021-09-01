import pandas as pd
import json
import ast 

df = pd.read_csv("publications-list.csv")

sources_set = set()
sources2publications = {}

for i in range(len(df['Sources'])):
    lst = ast.literal_eval(df['Sources'][i]) 
    
    for j in lst:
        if j not in sources_set:
            sources_set.add(j)
            sources2publications[j] = []

        sources2publications[j].append(i)

source_names = []

for source in sources2publications:
    source_names.append(source)

pub_contents = []

for source, publications in sources2publications.items(): 
    pub_content = []
    for publication in publications:
        pub_content.append([df['Title'][publication], df['URL'][publication]])
        
    pub_contents.append(pub_content)

df = pd.DataFrame({'Source':source_names, 'Publications': pub_contents})

df.to_csv('source2publications.csv')

print(sources2publications)