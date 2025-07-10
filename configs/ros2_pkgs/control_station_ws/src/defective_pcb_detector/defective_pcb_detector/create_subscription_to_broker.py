import requests
import json

url = "http://localhost:1026/ngsi-ld/v1/subscriptions/"

payload = json.dumps({
  "description": "Monitor changes to the image URL of PCB",
  "type": "Subscription",
  "entities": [
    {
      "type": "Robot",
      "id": "urn:ngsi-ld:pcb:1"
    }
  ],
  "watchedAttributes": [
    "mypcb"
  ],
  "notification": {
    "attributes": [
      "mypcb"
    ],
    "format": "keyValues",
    "endpoint": {
      "uri": "http://localhost:3000/update_image",
      "accept": "application/json"
    }
  }
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
