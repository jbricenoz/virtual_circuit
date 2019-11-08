import pytest
import requests
import json
from server import app


@pytest.fixture
def supply_url():
	return "http://0.0.0.0:8000/virtual-circuit/"

@pytest.mark.parametrize("src_port, dest_port",[(8000,8000)])
def test_response_ok(supply_url, src_port, dest_port):
	url = supply_url + str(src_port) + "/" + str(dest_port)
	data = {
        "term": 3,
        "speed": "50Mbps",
        "description": "Hola",
    }
	resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
	j = json.loads(resp.text)
	assert resp.status_code == 200, resp.text
    

@pytest.mark.parametrize("src_port, dest_port",[(8000,8000)])
def test_invalid_bandwith(supply_url, src_port, dest_port):
	url = supply_url + str(src_port) + "/" + str(dest_port)
	data = {
        "term": 3,
        "speed": "10Mbps",
        "description": "Hola",
    }
	resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
	# j = json.loads(resp.text)
	print(str(resp.text))
	assert resp.status_code == 400, resp.text
	assert str(resp.text) == "Error: Invalid Speed provided: 10Mbps", resp.text


@pytest.mark.parametrize("src_port, dest_port",[(8000,8000)])
def test_invalid_term(supply_url, src_port, dest_port):
	url = supply_url + str(src_port) + "/" + str(dest_port)
	data = {
        "term": 0,
        "speed": "50Mbps",
        "description": "Hola",
    }
	resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
	# j = json.loads(resp.text)
	assert resp.status_code == 400, resp.text
	assert str(resp.text) == "Error: term must be greater than 0", resp.text


@pytest.mark.parametrize("src_port, dest_port",[(8000,8000)])
def test_invalid_src_port(supply_url, src_port, dest_port):
	url = supply_url + str(src_port) + "/" + str(dest_port)
	data = {
        "term": 1,
        "speed": "50Mbps",
        "description": "Hola",
    }
	resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
	assert resp.status_code == 400, resp.text
	assert str(resp.text) == "Error: src_port must be a positive integer", resp.text

@pytest.mark.parametrize("src_port, dest_port",[(8000,000)])
def test_invalid_dest_port(supply_url, src_port, dest_port):
	url = supply_url + str(src_port) + "/" + str(dest_port)
	data = {
        "term": 1,
        "speed": "50Mbps",
        "description": "Hola",
    }
	resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
	assert resp.status_code == 400, resp.text
	assert str(resp.text) == "Error: dest_port must be a positive integer", resp.text

@pytest.mark.parametrize("src_port, dest_port",[(8000,9000)])
def test_invalid_json_format(supply_url, src_port, dest_port):
	url = supply_url + str(src_port) + "/" + str(dest_port)
	data = {
		"term": 1,
        "speed": "50Mbps",
        "description": "Hola",
    }
	resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
	assert resp.status_code == 400, resp.text
	assert str(resp.text) == "Error: Failed when parsing body as json", resp.text