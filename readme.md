### Run containers
1 - Initially build the docker file
 ```bash
sudo docker compose build
```
2 - run the container
 ```bash
sudo docker compose up
```
#### Run ROS2 pakcages
3 - In case you need source the workspaces
```bash
sudo docker exec -it pcbinfo bash
source /opt/vulcanexus/jazzy/setup.bash
source /control_station_ws/install/setup.bash
```

4 - In a new terminal, run the server where pcb images are uploaded

```bash
sudo docker exec -it pcbinfo bash
python3 -m uvicorn pcb_img_server.run_server:app --host 0.0.0.0 --port 5000
```


5- In a new termianl, launch the following for pcb images to get generated and sent to the server  

```bash
sudo docker exec -it pcbinfo bash
ros2 launch defective_pcb_detector defective_pcb_generator.launch.py
```
##### Some useful command on docker
6 - useful commands for docker
```bash
pip install --break-system-packages requests

11  - sudo docker compose -f docker-composev2.yml up -d


sudo docker stop $(sudo docker ps -q)

sudo docker ps

sudo docker logs -f orion_dds_test-orion-1
sudo docker stop $(sudo docker ps -q | tail -n +2)
```


7 - Create the subscription of quantumleap to the Orion-ld,
the endpoint should be the one which is reachable within 'mynet' network, you can run this python script 
```bash
python3 ./configs/contextbroker/QL_subscription_request.py
```
or the following command on the terminal.

```bash
curl --location 'http://localhost:1026/ngsi-ld/v1/subscriptions/' \
--header 'Content-Type: application/json' \
--data '{
  "description": "Monitor changes to the image URL of PCB",
  "type": "Subscription",
  "entities": [
    {
      "type": "Robot",
      "id": "urn:ngsi-ld:pcb:1"
    }
  ],
  "watchedAttributes": ["mypcb"],
  "notification": {
    "attributes": ["mypcb"],
    "endpoint": {
      "uri": "http://quantumleap:8668/v2/notify",
      "accept": "application/json"
    }
  }
}'
```


8 - if you want, you can check the subscription 
```bash
curl --location 'http://localhost:8668/v2/entities/urn:ngsi-ld:pcb:1/attrs/mypcb?lastN=3' \
--header 'Accept: application/json'
```

9 - check the list of subscriptions to the CB, run this 
```bash
python3 ./configs/contextbroker/Orion_ld_list_of_subscriptions.py.py
```
or 
```bash
curl --location 'http://localhost:1026/ngsi-ld/v1/subscriptions/' \
--header 'Content-Type: application/json'

```
9 - grafana query request

```bash
SELECT 
  mypcb['defected'] AS defected,
  mypcb['material_info'] AS material_info,
  mypcb['heatsink_number'] AS heatsink_size,
  mypcb['url'] AS image_url,
  mypcb['id'] AS pcb_id,
  mypcb['defect_loc_x'] AS x,
  mypcb['defect_loc_y'] AS y,
  mypcb['departured'] AS departured
FROM "doc"."etrobot"
WHERE mypcb['url'] IS NOT NULL
ORDER BY time_index DESC
LIMIT 1;
```

then choose Business Text plugin, and copy this html code for rendering of json info
```bash
      <h2>Defective PCB Info</h2>
      <p><strong>ID:</strong> {{@root.pcb_id}}</p>
      <p><strong>Defected:</strong> {{@root.defected}}</p>
      <p><strong>Material:</strong> {{@root.material_info}}</p>
      <p><strong>Defect Location:</strong> ({{@root.x}}, {{@root.y}})</p>
      <p><strong>Departured:</strong> {{@root.departured}}</p>

      <figure style="text-align: center;">
        <img src="{{{ @root.image_url }}}" alt="Defective PCB" width="400" style="border: 1px solid #ccc;" />
        <figcaption style="font-size: 14px; color: #666; margin-top: 8px;">
          Defective PCB detected on {{@root.departured}}
        </figcaption>
      </figure>



      ```json
      {{{json @root}}}
      ```
```

sudo docker rm -f grafana
docker run -d \
  --name=grafana \
  -p 3000:3000 \
  -e "GF_INSTALL_PLUGINS=marcusolsson-dynamictext-panel" \
  grafana/grafana

##

curl --location 'http://localhost:1026/ngsi-ld/v1/subscriptions/' \
--header 'Content-Type: application/json' \
--data '{
  "description": "Monitor changes to the image URL of PCB",
  "type": "Subscription",
  "entities": [
    {
      "type": "Robot",
      "id": "urn:ngsi-ld:pcb:1"
    }
  ],
  "watchedAttributes": ["mypcb"],
  "notification": {
    "attributes": ["mypcb"],
    "endpoint": {
      "uri": "http://localhost:8868/v2/notify",
      "accept": "application/json"
    }
  }
}'


curl --location 'http://localhost:8868/v2/entities/urn:ngsi-ld:pcb:1/attrs/mypcb?lastN=3' \
--header 'Accept: application/json'