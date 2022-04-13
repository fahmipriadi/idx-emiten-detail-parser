import json
import re
import csv
import pandas as pd
from jsonbender import bend, K, S, F
from os import listdir
from os.path import isfile, join
mypath = "/home/fahmipriadi/data"
#mypath = "/home/fahmipriadi/data2"

all = pd.read_csv('csv/all.csv')

kode_emiten = all['code'].values

for code in kode_emiten:
	#print(f"{code}")
	f = open(f"data/{code}.json")
	data = json.load(f)
	if code != data["Profiles"][0]["KodeEmiten"]:
		print(code)

