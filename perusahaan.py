import json
import re
import csv
from jsonbender import bend, K, S, F
from os import listdir
from os.path import isfile, join
mypath = "/home/fahmipriadi/data"
#mypath = "/home/fahmipriadi/data2"


onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)

nodes = []
links = []

low = lambda a : a.lower()

group = ["Sekretaris", "Direktur", "Komisaris", "KomiteAudit","AnakPerusahaan","PemegangSaham"]

for x in onlyfiles:
	# Opening JSON file
	f = open(f"data/{x}")
	#f = open(f"data2/{x}")
	 	
	

	# returns JSON object as
	# a dictionary
	data = json.load(f)
	

	#json bender template to map company information 
	mapping_nodes_emiten = {
    		'id':  K(data["Profiles"][0]["KodeEmiten"]),
    		'group': K('Perusahaan')
	}


	#mapping_links = {
    	#	'target': S('Nama') >> F(low),
    	#	'source': K(data["Profiles"][0]["KodeEmiten"]),
	#}
	#end of json bender template
	
	# use template to pull company data and add to nodes
	resultEmiten = bend(mapping_nodes_emiten, data)
	nodes.append(resultEmiten)
	
	for g in group:	
		
		#pull entities inside company and add to nodes and links

		#template to map subsidiaries
		mapping_nodes_anak = {
    			'id': S('Nama') >> F(low),
    			'group': K('Perusahaan')
		}
		

		#template to map person or other business entities
		mapping_nodes_orang = {
    			'id': S('Nama') >> F(low),
    			'group': K('Orang')
		}

		#json bender template to map links with type
		
		mapping_links_g = {
    			'target': S('Nama') >> F(low),
    			'source': K(data["Profiles"][0]["KodeEmiten"]),
			'type': K(g)
		}
		
		entity = data[f"{g}"]
		for e in entity:
			if e["Nama"].lower() not in [	"saham treasury",
							"0","n/a","tidak ada","","(-)",".","--","'-","-",
							"dplk bank rakyat indonesia - saham syariah",
							"dp bukit asam",
							"pemegang saham di bawah 5%",
							"p.saham di bawah 5%",
							"asing"
							]:
				if not ((re.search(r'masyarakat' ,e["Nama"].lower())) 
					or (re.search(r'lainnya' ,e["Nama"].lower()))
					or (re.search(r'lain-lain' ,e["Nama"].lower()))
					or (re.search(r'ketenagakerjaan' ,e["Nama"].lower()))
					or (re.search(r'asset management' ,e["Nama"].lower()))
					or (re.search(r'yayasan' ,e["Nama"].lower()))
					or (re.search(r'publik' ,e["Nama"].lower()))
					or (re.search(r'public' ,e["Nama"].lower()))
					or (re.search(r'simas' ,e["Nama"].lower()))
					or (re.search(r'dapen' ,e["Nama"].lower()))
					or (re.search(r'koperasi' ,e["Nama"].lower()))
					or (re.search(r'komisaris' ,e["Nama"].lower()))
					or (re.search(r'karyawan' ,e["Nama"].lower()))
					or (re.search(r'direksi' ,e["Nama"].lower()))
					or (re.search(r'fund' ,e["Nama"].lower()))
					or (re.search(r'sekuritas' ,e["Nama"].lower()))
					or (re.search(r'pensiun' ,e["Nama"].lower()))
					or (re.search(r'pemodal' ,e["Nama"].lower()))
					or (re.search(r'\-$' ,e["Nama"].lower()))
					): 
					
						if g in ["AnakPerusahaan"]:
						
							resultNodes = bend(mapping_nodes_anak, e)
						else:
							resultNodes = bend(mapping_nodes_orang, e)
				
						resultLinks = bend(mapping_links_g, e)
						nodes.append(resultNodes)
						links.append(resultLinks)			
		
	
	f.close()

# remove duplicates from node

uniqueNodes = { each['id'] : each for each in nodes }.values()
# uniqueLinks = { each['id'] : each for each in nodes }.values()


toJSON = json.dumps(list(uniqueNodes))
uniqueJSON = json.loads(toJSON)



#combine nodes and links

graph = {
		"nodes": uniqueJSON,
		"links": links
	}

with open("graph/perusahaan.json",'w') as outfile:
#with open("graph/perusahaan_data2.json",'w') as outfile:
	json.dump(graph, outfile)

fieldnames = ["id","group"]

# open the file in the write mode
#with open('csv/nodes_analysis.csv', 'w', encoding='UTF8', newline='') as f:
#    writer = csv.DictWriter(f, fieldnames=fieldnames)
#    writer.writeheader()
#    writer.writerows(uniqueJSON)
