#import cloudscraper
import requests
import pandas as pd
import json
from time import sleep
from urllib.parse import urlencode

NUM_RETRIES = 3
API_KEY = '48edadd474784c2989c333bbe9dd81a0693460e307d'


all = pd.read_csv('data/continue.csv')
#all = pd.read_csv('data/few.csv')

kode_emiten = all['code'].values

for code in kode_emiten:
	print(f"{code}")
	url = f"https://idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?kodeEmiten={code}"
	params = {'token': API_KEY, 'url': url, 'render': 'true'}
	for _ in range(NUM_RETRIES):
		try:
			#result = scraper.get('http://api.scraperapi.com/', params=urlencode(params)) 
			result = requests.get('http://api.scrape.do/', params=urlencode(params)) 
			if result.status_code in [200, 404]:
				break
		except requests.exceptions.ConnectionError:
			response = ''
			print("Connection Error")

	#result = scraper.get(f"https://idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?kodeEmiten={code}") 
	# result = scraper.get(f"http://api.scraperapi.com?api_key=d294f4496509d968ab9b9bda6938d9ba&url=https://idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?kodeEmiten={code}", headers={'Cache-Control': 'no-cache'}) 
	print(result.status_code)
	if result.status_code == 200:
		print(result.text.encode('utf8'))
		# print(result.text)
		# print(result.content)
		# result = json.loads(result.text) 
		# print(result['Search'])
		#with open(f"data/{code}.json", 'w') as outfile:
		#	json.dump(result, outfile)
	#sleep(5)
