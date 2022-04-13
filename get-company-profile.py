import json
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver import Chrome
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

def status_code_first_request(performance_log):
    """
        Selenium makes it hard to get the status code of each request,
        so this function takes the Selenium performance logs as an input
        and returns the status code of the first response.
    """
    for line in performance_log:
        try:
            json_log = json.loads(line['message'])
            if json_log['message']['method'] == 'Network.responseReceived':
                return json_log['message']['params']['response']['status']
        except:
            pass
    return json.loads(response_received[0]['message'])['message']['params']['response']['status']

## enable Selenium logging
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

API_KEY = 'd294f4496509d968ab9b9bda6938d9ba'

# scrapeAPI
proxy_options = {
    'proxy': {
        'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
	'no_proxy': 'localhost,127.0.0.1'
    }
}

# 

#scrape.do
#API_KEY = '48edadd474784c2989c333bbe9dd81a0693460e307d'
#proxy_options = {
#    'proxy': {
#	'http': f'http://{API_KEY}:render=false&customHeaders=false@proxy.scrape.do:8080',
#	'no_proxy': 'localhost,127.0.0.1'
#    }
#}

NUM_RETRIES = 2

# http client
http = webdriver.Chrome(ChromeDriverManager().install(),
		desired_capabilities=caps,
		seleniumwire_options=proxy_options)

all = pd.read_csv('data/all.csv')
# all = pd.read_csv('data/few.csv')

# get kode-kode emiten
kode_emiten = all['code'].values

for code in kode_emiten:
	# link
	link = f"https://idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?kodeEmiten={code}"

	# send request
	# always try to repeat
	# request whenever failed
	#while True:
	for _ in range(NUM_RETRIES):
		try:
			# send request
			http.get(link)
			performance_log = http.get_log('performance')
			status_code = status_code_first_request(performance_log)
			# Get data
			if status_code in [200, 404]:
                    		## escape for loop if the API returns a successful response
                    		break
			# result = json.loads(result)
			# success, we stop the while loop
			break
		except NoSuchElementException:
			print(f"Failed to get data for {code}")
			print(http.page_source)
			break
		except requests.exceptions.ConnectionError:
                	driver.close()
		# except:
			# error, we sleep for 2 minutes
			# sleep(2*60)

	# ada isinya?
	if status_code == 200:
		result = http.find_element(By.CSS_SELECTOR, "pre").text
		print(result)
		result = json.loads(result)
		print(f"{code}")
		with open(f"data/{code}.json", 'w') as outfile:
    			json.dump(result, outfile)
