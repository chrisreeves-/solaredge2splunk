import datetime
import http.client
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Remove unverified HTTPS request warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

solaredgeurl = "monitoringapi.solaredge.com"
solaredgesite = "xxxxxxx"
solaredgeapikey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
splunkurl = "splunk.example.com:888"
splunkapi = "Splunk xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

year = datetime.datetime.now().year
month = datetime.datetime.now().month
hour = datetime.datetime.now().hour
day = datetime.datetime.now().day
startmin = datetime.datetime.now().minute - 15
endmin = datetime.datetime.now().minute

# Get 15 minute chunk of data from SolarEdge
conn = http.client.HTTPSConnection(solaredgeurl)
payload = ''
headers = {'Accept': 'application/json'}
conn.request("GET", f"/site/{solaredgesite}/power?startTime={year}-{month}-{day}%20{hour}:{startmin}:00&endTime={year}-{month}-{day}%20{hour}:{endmin}:00&api_key={solaredgeapikey}", payload, headers)
res = conn.getresponse()
data = res.read()

# Send data to Splunk
splunkurl=f'https://{splunkurl}/services/collector/event'
authHeader = {'Authorization': f'{splunkapi}'}
powerstats = {"event": data.decode('utf8'), "sourcetype": "lambda"}
sendtosplunk = requests.post(splunkurl, headers=authHeader, json=powerstats, verify=False)
if sendtosplunk.status_code == 200:
    print("Posted successfully to " + sendtosplunk.url)
elif sendtosplunk.status_code >= 400:
    print("Failed to send data to " + sendtosplunk.url)
