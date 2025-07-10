import requests
import json

url = "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:pcb:1?options=keyValues"

payload = {}
headers = {

}

response = requests.request("GET", url, headers=headers, data=payload)

tt = response.json()
print(tt["mypcb"]["url"])