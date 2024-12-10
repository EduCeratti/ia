import requests
from requests.exceptions import SSLError
url = "https://example.com/"
try:
    # Make a request with SSL verification enabled
    response = requests.get(url)
    print("Request succeeded. Response code:", response.status_code)
except SSLError as e:
    print("SSL error:", e)
try:
    # Make a request with SSL verification disabled
    response = requests.get(url, verify=False)
    print("Request succeeded (without SSL verification). Response code:", response.status_code)
except requests.exceptions.RequestException as e:
    print("Request failed:", e)