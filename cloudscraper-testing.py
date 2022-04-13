#import cloudscraper
import requests
import pandas as pd
import json
from time import sleep
from urllib.parse import urlencode

NUM_RETRIES = 3
API_KEY = 'd294f4496509d968ab9b9bda6938d9ba'

# http_proxy = f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001'

http_proxy = f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001'
# https_proxy = f'https://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001'

# http_proxy  = f'http://48edadd474784c2989c333bbe9dd81a0693460e307d@proxy.scrape.do:8080'

proxyDict = { 
              "http"  : http_proxy 
            }

all = pd.read_csv('data/continue.csv')
#all = pd.read_csv('data/few.csv')

kode_emiten = all['code'].values

for code in kode_emiten:
	#scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
	#scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
	print(f"{code}")
	#result = scraper.get(f"https://idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?kodeEmiten={code}", proxies=proxyDict) 
	url = f"https://idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?kodeEmiten={code}"
	params = {'api_key': API_KEY, 'url': url, 'render': 'true'}
	for _ in range(NUM_RETRIES):
		try:
			#result = scraper.get('http://api.scraperapi.com/', params=urlencode(params)) 
			result = requests.get('http://api.scraperapi.com/', params=urlencode(params)) 
			if result.status_code in [200, 404]:
				break
		except requests.exceptions.ConnectionError:
			response = ''
			print("Connection Error")

	#result = scraper.get(f"https://idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?kodeEmiten={code}") 
	# result = scraper.get(f"http://api.scraperapi.com?api_key=d294f4496509d968ab9b9bda6938d9ba&url=https://idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?kodeEmiten={code}", headers={'Cache-Control': 'no-cache'}) 
	print(result.status_code)
	if result.status_code == 200:
		print(result.text)
		print(result.content)
		result = json.loads(result.text) 
		print(result['Search'])
		with open(f"data/{code}.json", 'w') as outfile:
			json.dump(result, outfile)
	#sleep(5)
