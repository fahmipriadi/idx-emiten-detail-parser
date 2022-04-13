import json
import re
from jsonbender import bend, K, S, F
from os import listdir
from os.path import isfile, join
mypath = "/home/fahmipriadi/data"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)

nodes = []
links = []

low = lambda a : a.lower()

group = ["Sekretaris", "Direktur", "Komisaris", "Komisaris", "KomiteAudit","AnakPerusahaan","PemegangSaham"]

for x in onlyfiles:
	# Opening JSON file
	f = open(f"data/{x}")
 	
	# returns JSON object as
	# a dictionary
	data = json.load(f)
	
	mapping_nodes_emiten = {
    		'id':  K(data["Profiles"][0]["NamaEmiten"].lower()),
    		'group': K('Perusahaan')
	}


	mapping_links = {
    		'target': S('Nama') >> F(low),
    		'source': K(data["Profiles"][0]["NamaEmiten"].lower())
	}

	
	# pull company data and add to nodes
	resultEmiten = bend(mapping_nodes_emiten, data)
	nodes.append(resultEmiten)
	
	for g in group:	
		
		#pull entities inside company and add to nodes and links
		mapping_nodes_anak = {
    			'id': S('Nama') >> F(low),
    			'group': K('Perusahaan')
		}
		
		mapping_nodes_orang = {
    			'id': S('Nama') >> F(low),
    			'group': K('Orang')
		}
		
		entity = data[f"{g}"]
		for e in entity:
			if e["Nama"].lower() not in ["saham treasury","publik","0","n/a","tidak ada","","-"]:
				if not ((re.search(r'masyarakat' ,e["Nama"].lower())) 
					or (re.search(r'lainnya' ,e["Nama"].lower()))
					or (re.search(r'lain-lain' ,e["Nama"].lower()))): 
					if g in ["AnakPerusahaan"]:
						
						resultNodes = bend(mapping_nodes_anak, e)
					else:
						resultNodes = bend(mapping_nodes_orang, e)
				
					resultLinks = bend(mapping_links, e)
					nodes.append(resultNodes)
					links.append(resultLinks)			
		
	
	f.close()

# remove duplicates from node

uniqueNodes = { each['id'] : each for each in nodes }.values()
# uniqueLinks = { each['id'] : each for each in nodes }.values()

dict(sorted(uniqueNodes.items(), key=lambda item: item[1]))
print(uniqueNodes)

toJSON = json.dumps(list(uniqueNodes))
uniqueJSON = json.loads(toJSON)

#combine nodes and links

graph = {
		"nodes": uniqueJSON,
		"links": links
	}

# with open("graph/perusahaan.json",'w') as outfile:
# 	json.dump(graph, outfile)

