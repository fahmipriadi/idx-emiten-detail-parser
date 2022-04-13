from lxml import html
import requests
import pandas as pd
import json
from time import sleep
from urllib.parse import urlencode

NUM_RETRIES = 3
fahmipriadi_API_KEY = '61c7dbbd43f4812f1fe5eb9d'
davhay_API_KEY = '61ce7e1cc18e762580207d18'
wilayahbabel_API_KEY = '61ceaa67ae612e333cda9bdd'
hasvan24_API_KEY = '61ceb710fdfd9638ac1e4742'

all = pd.read_csv('csv/remainingbroker.csv')
#all = pd.read_csv('csv/allbroker.csv')

#all = pd.read_csv('data/few.csv')

kode_emiten = all['code'].values

for code in kode_emiten:
	print(f"{code}")

	url = f"https://www.idx.co.id/umbraco/Surface/ExchangeMember/GetBrokerDetail?code={code}"
	params = {'api_key': fahmipriadi_API_KEY, 'url': url}
	for _ in range(NUM_RETRIES):
		try:
			result = requests.get('https://api.scrapingdog.com/scrape', params=urlencode(params)) 
			if result.status_code in [200, 404]:
				break
		except requests.exceptions.ConnectionError:
			response = ''
			print("Connection Error")

	print(result.status_code)
	if result.status_code == 200:
		#print(result.text)
		page = html.fromstring(result.text)
		#try:
		print(page.cssselect('pre')[0].text_content())
		data = json.loads(page.cssselect('pre')[0].text_content())
		#print(data["Search"])
		print(data)
		with open(f"databroker/{code}.json", 'w') as outfile:
			json.dump(data, outfile)

		#except:
		#	print("Save to txt")
		#	with open(f"txtbroker/{code}.txt", 'w') as outfile:
                #                outfile.write(page.cssselect('pre')[0].text_content())		
	#sleep(5)
