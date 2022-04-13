import requests

url = "https://idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail"

querystring = {"kodeEmiten":"WSBP"}

headers = {
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response)
