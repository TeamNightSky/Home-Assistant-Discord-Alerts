import os
import json
import requests
from .utils import DATA


TOKEN = os.getenv("HOMEASSISTANT_TOKEN")
URL = DATA['api-endpoint']

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "content-type": "application/json",
}


def update_config():
    url = os.path.join(URL, 'config')
    resp = requests.get(url, headers=HEADERS)
    try:
        resp.json()
    except json.decoder.JSONDecodeError:
        print(resp.text)
        return
    for k,v in resp.json().items():
        DATA[k] = v
    DATA.save()


update_config()
    

def get_services():
    url = os.path.join(URL, 'services')
    resp = requests.get(url, headers=HEADERS)
    data = resp.json()
    data = {domain['domain']: domain for domain in data}
    return data


def run_service(domain, script_name):
    url = os.path.join(URL, 'services', domain, script_name)
    resp = requests.post(url, headers=HEADERS)
    return resp.json()


run_script = lambda x: run_service('script', x)
get_scripts = lambda: list(get_services()['script']['services'])
