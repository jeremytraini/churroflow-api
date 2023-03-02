import requests
import json
from src import config


def health_check_v1(): 
    response = requests.get(config.url + 'health_check/v1')

    return json.loads(response.text)


# Sample calls below

def sample_clear():
    requests.delete(config.url + 'test/delete/v1')

def sample_post(val):
    payload = {
        "key": val
    }
    response = requests.post(config.url + 'test/post/v1', json=payload)

    return json.loads(response.text)

def sample_get(val): 
    payload = {
        "key": val
    }
    response = requests.get(config.url + 'test/get/v1', params=payload)

    return json.loads(response.text)

def sample_put(val): 
    payload = {
        "key": val
    }
    response = requests.put(config.url + 'test/put/v1', json=payload)

    return json.loads(response.text)

def sample_delete(val):
    payload = {
        "key": val
    }

    response = requests.delete(config.url + 'test/delete/v1', json=payload)

    return json.loads(response.text)
