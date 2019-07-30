#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: pranaydogra
"""
import warnings
warnings.filterwarnings("ignore")
import networkx as nx
import matplotlib.pyplot as plt
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from itertools import permutations
from collections import Counter
# =============================================================================
# Define functions to use is script
# =============================================================================
# Search PubMed for all authors associated with person(s) of interest
def all_names(t_lst):
    names_list = []
    for term in t_lst:
        driver.get("https://www.ncbi.nlm.nih.gov/pubmed")
        inputElement = driver.find_element_by_id("term")
        inputElement.send_keys(term)
        inputElement.send_keys(Keys.ENTER)
        display = driver.find_element_by_css_selector('ul.left > li:nth-child(3) > a:nth-child(1) > span:nth-child(1)')
        display.click()
        time.sleep(3)
        num_results = driver.find_element_by_xpath('//*[@id="display_settings_menu_ps"]/fieldset/ul/li[6]/label')
        num_results.click()
        res = int(driver.find_element_by_xpath('//*[@id="maincontent"]/div/div[3]/div/h3').text.split(':')[1].strip())
        text_only = []
        if res < 50:
            for i in range(1,(int(res) + 1)):
                content = driver.find_element_by_xpath('//*[@id="maincontent"]/div/div[5]/div[{}]/div[2]/div[1]/p[1]'. format(i))
                text_only.append(content.text)
        else:
            for i in range(1,51):
                content = driver.find_element_by_xpath('//*[@id="maincontent"]/div/div[5]/div[{}]/div[2]/div[1]/p[1]'. format(i))
                text_only.append(content.text)
        for elements in text_only:
           auth_list = elements.split(',')
           auth_list = [x.strip(' ') for x in auth_list]
           auth_list = [x.strip('.') for x in auth_list]
           names_list.append(auth_list)
    
    return names_list

# Clean list of names to remove middle initial issues
def clean_names(lst):
    short_names = []
    for name in lst:
        caps =  list(c for c in name if c.isupper())
        if '-' not in name and len(caps) == 3: 
            new_name = re.sub(r'(.*){}'.format(caps[-1]), r'\1', name).strip()
            short_names.append(new_name)
        elif '-' not in name and len(caps) == 4:
            new_name = re.sub(r'(.*){}'.format(caps[-1]), r'\1', name).strip()
            new_name = re.sub(r'(.*){}'.format(caps[-2]), r'\1', new_name).strip()
            short_names.append(new_name)
        elif '-' not in name and len(caps) == 5:
            new_name = re.sub(r'(.*){}'.format(caps[-1]), r'\1', name).strip()
            new_name = re.sub(r'(.*){}'.format(caps[-2]), r'\1', new_name).strip()
            new_name = re.sub(r'(.*){}'.format(caps[-3]), r'\1', new_name).strip()
            short_names.append(new_name)
        elif '-' in name and len(caps) > 3:
            new_name = re.sub(r'(.*){}'.format(caps[-1]), r'\1', name).strip()
            short_names.append(new_name)
        else:
            short_names.append(name)
    
    return short_names

# Find the shortest link between authors
def shortest_link():
    q_auth = input(r"Enter query author (last name space first initial): ")
    l_auth = input(r"Enter connected-to author (last name space first initial): ")
    
    for path in nx.all_shortest_paths(g, source = q_auth, target = l_auth):
        print(path)

# =============================================================================
# load chrome driver options to open webpage in background
# =============================================================================
window_size = "1920,1080"
options = Options()
options.add_argument("--headless")
options.add_argument("--wind-size = {}" . format(window_size))
driver = webdriver.Chrome(executable_path = 'ENTER PATH TO YOUR CHROME DRIVER LOCATION',
                          options = options)

# =============================================================================
# Search for author on PubMed
# =============================================================================
searchterm = input(r"Enter author names separated by comma (,): ")
out_dir = input(r"Enter path to output directory: ")
searchterm = searchterm.split(',')

# get list of all authors
all_authors = all_names(searchterm)

# clean the names
new_names = [clean_names(item) for item in all_authors]
#print(new_names) #Print here a list of authors associated with the author in question

connection_list = []
for lst in new_names:
    connections = list(permutations(lst,2))
    for e in connections:
        connection_list.append(e)

connection_instances = Counter(connection_list)
           
edges = []
for k,v in connection_instances.items():
    edges.append((k[0],k[1], {'weight':v}))

g = nx.Graph()
g.add_edges_from(edges)

# estimate connectedness between graph nodes (each paper contribues 2 weight)
well_connected = [(s, t) for (s, t, w) in g.edges(data=True) if w['weight'] >= 3]
others = [(s, t) for (s, t, w) in g.edges(data=True) if w['weight'] < 3]

# determine the positon of the nodes (once satsfied by node postion do no run this again)
k = 0.2
pos = nx.spring_layout(g,weight='weight', k = k)

# initiate and plot the figure
plt.figure(figsize=(10, 10))
nx.draw_networkx_nodes(g,pos, node_size= 50, alpha=1, node_color = 'SteelBlue')
nx.draw_networkx_edges(g, pos, edgelist = well_connected, edge_color="r", 
                       arrows=True, width=2,)
nx.draw_networkx_edges(g, pos, edgelist = others, edge_color= "k", 
                       arrows=True, width=0.5, style = "dashed")
nx.draw_networkx_labels(g, pos,font_size=12, font_color = "k")

plt.axis("off")
plt.savefig(out_dir + "{}_connections.svg" .format (searchterm), format = 'svg')
plt.ioff()
print("Plot saved to: {}" .format(out_dir))

# Find the shortest link between any two authors in the network
response = input(r"Search for shortest link between authors (y/n): ")

while response == 'y':
    shortest_link()
    response = input(r"Search for another shortest link between authors (y/n): ")
    
else:
    print("Thank you!")

plt.show()
