from lxml import html
import requests
import pandas as pd
import json
from time import sleep
from urllib.parse import urlencode

mypath="/home/fahmipriadi/data"

all = pd.read_csv('csv/continue.csv')
#all = pd.read_csv('data/few.csv')

onlyfiles = [f for f in listdir(mypath) if isFile(join(mypath, f))]

kode_emiten = all['code'].values

for downloaded in onlyfiles:
	
	print(f"{code}")

	
