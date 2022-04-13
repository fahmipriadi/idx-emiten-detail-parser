import json
import re
import csv
from jsonbender import bend, K, S, F
from os import listdir
from os.path import isfile, join
mypath = "/home/fahmipriadi/databroker"
#mypath = "/home/fahmipriadi/data2"


onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)

nodes = []
links = []

low = lambda a : a.lower()
rstrp = lambda a : a.rstrip()

group = ["ShareHolders", "Managements"]

for x in onlyfiles:
	# Opening JSON file
	f = open(f"databroker/{x}")
	#f = open(f"data2/{x}")
	 	
	
	# returns JSON object as
	# a dictionary
	data = json.load(f)
	#print(data)
	#json bender template to map company information 
	mapping_nodes_emiten = {
    		'id':  K(data["Name"].lower()),
		#'code': K(data["Code"]),
    		'group': K('Broker')
	}


	#mapping_links = {
    	#	'target': S('ShareHolderName') >> F(low),
    	#	'source': K(data["Profiles"][0]["KodeEmiten"]),
	#}
	#end of json bender template
	
	# use template to pull company data and add to nodes
	resultEmiten = bend(mapping_nodes_emiten, data)
	nodes.append(resultEmiten)
	
	for g in group:	
		if g == "ShareHolders":
			gg = "PemegangSaham"
			mapping_nodes_link = {
    				'id': S('ShareHolderName') >> F(low) >> F(rstrp),
    				'group': K('Perusahaan')
			}
			mapping_links_g = {
    				'target': S('ShareHolderName') >> F(low) >> F(rstrp),
    				'source': K(data["Name"].lower()),
				'type': K(gg)
			}
			entity = data[f"{g}"]			
			for e in entity:
				if e["ShareHolderName"].lower() not in ["saham treasury","0","n/a","tidak ada","","(-)",".","--","'-","-",
				                                        "pemegang saham di bawah 5%","p.saham di bawah 5%","masyarakat"]:
                    			if not ((re.search(r'masyarakat' ,e["ShareHolderName"].lower())) 
                                        or (re.search(r'lainnya' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'lain-lain' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'ketenagakerjaan' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'asset management' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'yayasan' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'publik' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'public' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'simas' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'dapen' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'koperasi' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'komisaris' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'karyawan' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'direksi' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'fund' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'sekuritas' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'pensiun' ,e["ShareHolderName"].lower()))
                                        or (re.search(r'\-$' ,e["ShareHolderName"].lower()))
                                        ):
						                    resultNodes = bend(mapping_nodes_link, e)
						                    resultLinks = bend(mapping_links_g, e)
						                    nodes.append(resultNodes)
						                    links.append(resultLinks)
		if g == "Managements":
			entity = data[f"{g}"]
			for e in entity:
				if (re.search(r'direktur' ,e["JobPositionName"].lower())):
					gg = "Direktur"
					mapping_nodes_link = {
    						'id': S('PersonName') >> F(low) >> F(rstrp),
    						'group': K('Orang')
					}
					mapping_links_g = {
    						'target': S('PersonName') >> F(low) >> F(rstrp),
    						'source': K(data["Name"].lower()),
						'type': K(gg)
					}
				if (re.search(r'komisaris' ,e["JobPositionName"].lower())):
					gg = "Komisaris"
					mapping_nodes_link = {
    						'id': S('PersonName') >> F(low) >> F(rstrp),
    						'group': K('Orang')
					}
					mapping_links_g = {
    						'target': S('PersonName') >> F(low) >> F(rstrp),
    						'source': K(data["Name"].lower()),
						'type': K(gg)
					}

				resultNodes = bend(mapping_nodes_link, e)
				resultLinks = bend(mapping_links_g, e)
				nodes.append(resultNodes)
				links.append(resultLinks)			
		
	f.close()

# remove duplicates from node

uniqueNodes = { each['id'] : each for each in nodes }.values()
# uniqueLinks = { each['id'] : each for each in nodes }.values()


toJSON = json.dumps(list(uniqueNodes))
uniqueJSON = json.loads(toJSON)

print(links)
print(uniqueJSON)
#combine nodes and links

graph = {
		"nodes": uniqueJSON,
		"links": links
	}

with open("graph/broker.json",'w') as outfile:
#with open("graph/perusahaan_data2.json",'w') as outfile:
	json.dump(graph, outfile)

#fieldnames = ["id","group"]

# open the file in the write mode
#with open('csv/nodes_analysis.csv', 'w', encoding='UTF8', newline='') as f:
#    writer = csv.DictWriter(f, fieldnames=fieldnames)
#    writer.writeheader()
#    writer.writerows(uniqueJSON)
#if e["ShareHolderName"].lower() not in [	"saham treasury",
#							"0","n/a","tidak ada","","(-)",".","--","'-","-",
#							"dplk bank rakyat indonesia - saham syariah",
#							"dp bukit asam",
#							"pemegang saham di bawah 5%",
#							"p.saham di bawah 5%"
#							]:
#				if not ((re.search(r'masyarakat' ,e["ShareHolderName"].lower())) 
#					or (re.search(r'lainnya' ,e["ShareHolderName"].lower()))
#					or (re.search(r'lain-lain' ,e["ShareHolderName"].lower()))
#					or (re.search(r'ketenagakerjaan' ,e["ShareHolderName"].lower()))
#					or (re.search(r'asset management' ,e["ShareHolderName"].lower()))
#					or (re.search(r'yayasan' ,e["ShareHolderName"].lower()))
#					or (re.search(r'publik' ,e["ShareHolderName"].lower()))
#					or (re.search(r'public' ,e["ShareHolderName"].lower()))
#					or (re.search(r'simas' ,e["ShareHolderName"].lower()))
#					or (re.search(r'dapen' ,e["ShareHolderName"].lower()))
#					or (re.search(r'koperasi' ,e["ShareHolderName"].lower()))
#					or (re.search(r'komisaris' ,e["ShareHolderName"].lower()))
#					or (re.search(r'karyawan' ,e["ShareHolderName"].lower()))
#					or (re.search(r'direksi' ,e["ShareHolderName"].lower()))
#					or (re.search(r'fund' ,e["ShareHolderName"].lower()))
#					or (re.search(r'sekuritas' ,e["ShareHolderName"].lower()))
#					or (re.search(r'pensiun' ,e["ShareHolderName"].lower()))
#					or (re.search(r'\-$' ,e["ShareHolderName"].lower()))
#					): 
#			
