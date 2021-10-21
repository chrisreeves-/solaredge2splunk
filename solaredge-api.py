import http.client
import json
import pytz
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

timezone = pytz.timezone('AUSTRALIA/Brisbane')

# Remove unverified HTTPS request warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

solaredgeurl = os.environ.get('solaredgeurl')
solaredgesite = os.environ.get('solaredgesite')
solaredgeapikey = os.environ.get('solaredgeapikey')
splunkuri = os.environ.get('splunkurl')
splunkapi = os.environ.get('splunkapi')

def data():
    # Get 15 minute chunk of data from SolarEdge
    conn = http.client.HTTPSConnection(solaredgeurl)
    payload = ''
    headers = {'Accept': 'application/json'}
    conn.request("GET", f"/site/{solaredgesite}/currentPowerFlow?api_key={solaredgeapikey}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    jsonfmt = json.loads(data.decode('utf8'))
    # Send data to Splunk
    splunkurl = f"https://{splunkuri}/services/collector/event"
    authHeader = {'Authorization': f'{splunkapi}'}
    powerstats = {"event": jsonfmt, "sourcetype": "lambda"}
    sendtosplunk = requests.post(splunkurl, headers=authHeader, json=powerstats, verify=False)
    # Error handling/reporting
    if sendtosplunk.status_code in range(200, 299):
        print("Posted successfully to " + sendtosplunk.url)
    elif sendtosplunk.status_code in range(300, 399):
        print("Redirect errors to " + sendtosplunk.url)
    elif sendtosplunk.status_code in range(429, 429):
        print("Too many API requests to " + sendtosplunk)
    elif sendtosplunk.status_code in range(400, 428 or 430, 499):
        print("Client errors to " + sendtosplunk.url)
    elif sendtosplunk.status_code in range(500, 599):
        print("Server errors to " + sendtosplunk.url)

def main(event, context):
    data()
