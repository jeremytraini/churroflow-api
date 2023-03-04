import requests
import json
from src.config import full_url


def health_check_v1(): 
    response = requests.get(full_url + 'health_check/v1')

    return json.loads(response.text)


# Sample calls below

def sample_clear():
    requests.delete(full_url + 'test/delete/v1')

def sample_post(val):
    payload = {
        "key": val
    }
    response = requests.post(full_url + 'test/post/v1', json=payload)

    return json.loads(response.text)

def sample_get(val): 
    payload = {
        "key": val
    }
    response = requests.get(full_url + 'test/get/v1', params=payload)

    return json.loads(response.text)

def sample_put(val): 
    payload = {
        "key": val
    }
    response = requests.put(full_url + 'test/put/v1', json=payload)

    return json.loads(response.text)

def sample_delete(val):
    payload = {
        "key": val
    }

    response = requests.delete(full_url + 'test/delete/v1', json=payload)

    return json.loads(response.text)
