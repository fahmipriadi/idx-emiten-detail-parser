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

datacsv = []
	

header = ["code", "industri", "sub-industri"]
with open('csv/classification.csv', 'w', encoding='UTF8') as f:
	writer = csv.writer(f)
    	# write the header
	writer.writerow(header)
	#print(datacsv)
    	# write the data
	for x in onlyfiles:
		datarow = []
		# Opening JSON file
		f = open(f"data/{x}")
		#f = open(f"data2/{x}")
		# returns JSON object as
		# a dictionary
		data = json.load(f)
		datarow.append(f"{data['Profiles'][0]['KodeEmiten']}")
		datarow.append(f"{data['Profiles'][0]['Industri']}")
		datarow.append(f"{data['Profiles'][0]['SubIndustri']}")
		print(datarow)
		#datacsv.append(datarow)
		writer.writerow(datarow)
	#writer.writerow(datacsv)
