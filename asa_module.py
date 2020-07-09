# This module contains various functions for interacting with the ASA REST API
import requests
import json
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def init_params(params):
    #This function initializes global variables used in every API call
    global host
    global username
    global password
    global base_url
    host = params['host']
    base_url = 'https://' + host
    username = params['username']
    password = params['password']
    

def get_response(url, method, username, password, payload=''):
    #This function makes an API call and returns the response
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'REST API Agent'}

    try:
        if payload == '':
            r = requests.request(method, url, auth=(username, password), headers=headers, verify=False, timeout=120)
        else:
            print(f"Sending payload:\n\n{json.dumps(payload, indent=4)}\n")
            r = requests.request(method, url, json=payload, auth=(username, password), headers=headers, verify=False, timeout=120)

    except requests.exceptions.RequestException as e:
        print("Request failed!")
        raise

    if r.status_code not in range(200, 205):
        print(f"Request failed! \t {r}")
        raise ValueError(r.text)

    else:
        print(f"Success! \t {r}\n")

    return r

def dns_client(payload):
    #This function is for querying and configuring the DNS client 
    method = payload['method'] 
    print(f"Method: {method.upper()}")

    if 'description' in payload.keys():
        description = payload['description']
        print(f"Description: {description}")

    if 'payload' in payload.keys():
        payload = payload['payload']

    else:
        payload = ''

    url = f"{base_url}/api/dns/client"
    print(f"URL: {url}\n")

    return get_response(url, method, username, password, payload)

def dns_client_servergroups(payload):
    #This function is for querying and configuring DNS server groups
    method = payload['method'] 
    print(f"Method: {method.upper()}")

    if 'objectId' in payload.keys():
        objectId = payload['objectId']
        print(f"objectId: {objectId}")

    if 'description' in payload.keys():
        description = payload['description']
        print(f"Description: {description}")

    if 'payload' in payload.keys():
        payload = payload['payload']

    else:
        payload = ''

    if (method in ('put','patch','delete')) or (method == 'get' and 'objectId' in locals()):
        url = f"{base_url}/api/dns/client/servergroups/{objectId}"

    elif (method == 'post') or (method == 'get' and not 'objectId' in locals()): 
        url = f"{base_url}/api/dns/client/servergroups"
    
    print(f"URL: {url}\n")
    return get_response(url, method, username, password, payload)

def ntp_servers(payload):
    #This function is for querying and configuring NTP servers
    method = payload['method'] 
    print(f"Method: {method.upper()}")

    if 'objectId' in payload.keys():
        objectId = payload['objectId']
        print(f"objectId: {objectId}")

    if 'description' in payload.keys():
        description = payload['description']
        print(f"Description: {description}")

    if 'payload' in payload.keys():
        payload = payload['payload']

    else:
        payload = ''

    if (method in ('put','patch','delete')) or (method == 'get' and 'objectId' in locals()):
        url = f"{base_url}/api/devicesetup/ntp/servers/{objectId}"

    elif (method == 'post') or (method == 'get' and not 'objectId' in locals()): 
        url = f"{base_url}/api/devicesetup/ntp/servers"
    
    print(f"URL: {url}\n")
    return get_response(url, method, username, password, payload)

def interfaces_physical(payload):
    #This function is for querying and configuring physical interfaces
    method = payload['method'] 
    print(f"Method: {method.upper()}")

    if 'objectId' in payload.keys():
        objectId = payload['objectId']
        print(f"objectId: {objectId}")

    if 'description' in payload.keys():
        description = payload['description']
        print(f"Description: {description}")

    if 'payload' in payload.keys():
        payload = payload['payload']

    else:
        payload = ''

    if (method in ('put','patch')) or (method == 'get' and 'objectId' in locals()):
        url = f"{base_url}/api/interfaces/physical/{objectId}" 

    elif method == 'get' and not 'objectId' in locals(): 
        url = f"{base_url}/api/interfaces/physical"

    print(f"URL: {url}\n")
    return get_response(url, method, username, password, payload)

def cert_keypair(payload):
    #This function is for querying and configuring RSA keypair
    method = payload['method'] 
    print(f"Method: {method.upper()}")

    if 'objectId' in payload.keys():
        objectId = payload['objectId']
        print(f"objectId: {objectId}")

    if 'description' in payload.keys():
        description = payload['description']
        print(f"Description: {description}")

    if 'payload' in payload.keys():
        payload = payload['payload']

    else:
        payload = ''

    if method in ('get','delete') and 'objectId' in locals():
        url = f"{base_url}/api/certificate/keypair/{objectId}"

    elif method in ('get','post') and not 'objectId' in locals(): 
        url = f"{base_url}/api/certificate/keypair"

    print(f"URL: {url}\n")
    return get_response(url, method, username, password, payload)

def cert_identity(payload):
    #This function is used for querying and configuring a self-signed certificate  
    method = payload['method'] 
    print(f"Method: {method.upper()}")

    if 'objectId' in payload.keys():
        objectId = payload['objectId']
        print(f"objectId: {objectId}")

    if 'description' in payload.keys():
        description = payload['description']
        print(f"Description: {description}")

    if 'payload' in payload.keys():
        payload = payload['payload']

    else:
        payload = ''

    if method in ('get','delete') and 'objectId' in locals():
        url = f"{base_url}/api/certificate/identity/{objectId}"

    elif method in ('get','post') and not 'objectId' in locals(): 
        url = f"{base_url}/api/certificate/identity"

    print(f"URL: {url}\n")
    return get_response(url, method, username, password, payload)

def routing_static(payload):
    #This function is used for querying and configuring static routes
    method = payload['method'] 
    print(f"Method: {method.upper()}")

    if 'objectId' in payload.keys():
        objectId = payload['objectId']
        print(f"objectId: {objectId}")

    if 'description' in payload.keys():
        description = payload['description']
        print(f"Description: {description}")

    if 'payload' in payload.keys():
        payload = payload['payload']

    else:
        payload = ''

    if (method in ('put','patch','delete')) or (method == 'get' and 'objectId' in locals()):
        url = f"{base_url}/api/routing/static/{objectId}"

    elif (method == 'post') or (method == 'get' and not 'objectId' in locals()): 
        url = f"{base_url}/api/routing/static"
    
    print(f"URL: {url}\n")
    return get_response(url, method, username, password, payload)

def send_cli(payload):
    #This function sends CLI commands as defined in payload
    method = payload['method']
    print(f"Method: {method.upper()}")

    if 'description' in payload.keys():
        description = payload['description']
        print(f"Description: {description}")

    if 'payload' in payload.keys():
        payload = payload['payload']

    url = f"{base_url}/api/cli"

    print(f"URL: {url}\n")
    return get_response(url, method, username, password, payload)

def write_config():
    #This function performs a 'wr mem' on the ASA to save configuration
    url = f"{base_url}/api/commands/writemem"
    print("Saving configuration...")
    response = get_response(url, 'post', username, password)
    print("\n")
