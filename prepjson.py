import json
from jsonbender import bend, K, S
from os import listdir
from os.path import isfile, join
mypath = "/home/fahmipriadi/data"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

nodes = []
links = []

group = ["Sekretaris", "Direktur", "Komisaris", "Komisaris", "KomiteAudit","AnakPerusahaan","PemegangSaham"]

for x in onlyfiles:
	# Opening JSON file
	f = open(f"data/{x}")
 	
	# returns JSON object as
	# a dictionary
	data = json.load(f)
	
	mapping_nodes_emiten = {
    		'id':  K(data["Profiles"][0]["NamaEmiten"]),
    		'group': K('Perusahaan')
	}


	mapping_links = {
    		'target': S('Nama'),
    		'source': K(data["Profiles"][0]["NamaEmiten"])
	}

	
	# pull company data and add to nodes
	resultEmiten = bend(mapping_nodes_emiten, data)
	nodes.append(resultEmiten)
	
	for g in group:	
		
		#pull entities inside company and add to nodes and links
		mapping_nodes = {
    			'id': S('Nama'),
    			'group': K(g)
		}
		
		entity = data[f"{g}"]
		for e in entity:
			if e["Nama"] not in ["Saham Treasury", "Masyarakat", "","-","MASYARAKAT", "Publik"]:
				resultNodes = bend(mapping_nodes, e)
				resultLinks = bend(mapping_links, e)
				nodes.append(resultNodes)
				links.append(resultLinks)			
		
	
	f.close()

#combine nodes and links

graph = {
		"nodes": nodes,
		"links": links
	}

with open("graph/data.json",'w') as outfile:
	json.dump(graph, outfile)

"""
Map these attributes below to d3.js attributes

create following group:

nodes
	- id (nama, nama perusahaan)
	- group (Komisaris, Sekretaris, Direktur, Anak Perusahaan)
	- radius

links 
	- source (for each nama perusahaan)
	- target (add target)
- Perusahaan
- Direktur
- Komisaris
"""
