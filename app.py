import connexion
import yaml
import requests
import datetime
import json
from connexion import NoContent
from pykafka import KafkaClient


STORE_SERVICE_RENTING_REQUEST_URL = "http://localhost:8090/report/renting_request"
STORE_SERVICE_CHARGING_BOX_STATUS = "http://localhost:8090/report/charging_box_status"
HEADERS = {"content-type": "application/json"}

with open('app_config.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())


def report_renting_request(rentingRequest):
    #response = requests.post(STORE_SERVICE_RENTING_REQUEST_URL, json=rentingRequest, headers=HEADERS)
    #print(rentingRequest)

    client = KafkaClient(hosts=app_config['datastore']['server'] + ':' + str(app_config['datastore']['port']))
    topic = client.topics[app_config['datastore']['topic']]
    producer = topic.get_sync_producer()
    msg = {"type": "rr",
           "datetime":
               datetime.datetime.now().strftime("%Y -%m-%dT%H:%M:%S"),
           "payload": rentingRequest}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return NoContent


def report_charging_box_status(chargingBoxStatus):
    #response = requests.post(STORE_SERVICE_CHARGING_BOX_STATUS, json=chargingBoxStatus, headers=HEADERS)
    #print(chargingBoxStatus)

    client = KafkaClient(hosts=app_config['datastore']['server'] + ':' + str(app_config['datastore']['port']))
    topic = client.topics[app_config['datastore']['topic']]
    producer = topic.get_sync_producer()
    msg = {"type": "cbs",
           "datetime":
               datetime.datetime.now().strftime("%Y -%m-%dT%H:%M:%S"),
           "payload": chargingBoxStatus}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    return NoContent


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)