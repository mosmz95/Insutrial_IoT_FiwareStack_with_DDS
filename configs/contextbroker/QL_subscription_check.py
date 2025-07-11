import requests

url = "http://localhost:8668/v2/entities/urn:ngsi-ld:pcb:1/attrs/mypcb?limit=1"

payload = {}
headers = {
  'Accept': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
