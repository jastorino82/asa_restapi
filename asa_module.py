# This module contains various functions for interacting with the ASA RESTCONF API
import requests
import json
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def init_params(params):
    #This function initializes global variables used in every API call
    global host
    global username
    global password
    host = params['host']
    username = params['username']
    password = params['password']
    

def get_response(url, method, username, password, payload=''):
    #This function makes an API call and returns the response
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'REST API Agent'}

    try:
        if payload == '':
            r = requests.request(method, url, auth=(username, password), headers=headers, verify=False, timeout=10)
        else:
            r = requests.request(method, url, json=payload, auth=(username, password), headers=headers, verify=False, timeout=60)

    except requests.exceptions.RequestException as e:
        print("Request failed. Terminating!")
        raise SystemExit(e)

    if r.status_code not in range(200, 205):
        print(f"Request failed. Terminating! \t {r}")
        raise SystemExit()

    else:
        print(f"Success! \t {r}")

    return r

def get_interfaces():
    #This function fetches information about an interface, and displays some key information about it
    url = f'https://{host}/api/interfaces/physical'
    
    print(f"Fetching interface information...\n")
    response = get_response(url, 'get', username, password)
    print("\n")
    interfaces = response.json()

    for interface in interfaces['items']:
        print(f"Interface: {interface['hardwareID']}")
        print(f"Interface Name: {interface['name']}")
        print(f"Description: {interface['interfaceDesc']}")
        if interface['securityLevel'] == -1:
            print(f"Security Level: Not Set")
        else:
            print(f"Security Level: {interface['securityLevel']}")
        print(f"Speed: {interface['speed']}")
        print(f"Duplex: {interface['duplex']}")
        if type(interface['ipAddress']) == dict and interface['ipAddress']['kind'] == 'DHCP':
            url = f"https://{host}/api/monitoring/ipaddress/{interface['name']}"
            response = get_response(url, 'get', username, password)
            ip = response.json()['ipAddress']
            netmask = response.json()['netmask']
            print(f"IPv4 Address: {ip}")
            print(f"Netmask: {netmask}")

        elif type(interface['ipAddress']) == dict and 'ip' in interface['ipAddress'].keys():
            print(f"IPv4 Address: {interface['ipAddress']['ip']['value']}")
            print(f"Netmask: {interface['ipAddress']['netMask']['value']}")
        print(f"Shutdown Status: {interface['shutdown']}")
        print("\n")

def config_interface(payload):
    #This function configures an existing interface defined in payload
    url = f"https://{host}/api/interfaces/physical/{payload['objectid']}"
    print(f"Attempting to configure interface {payload['intname']} as follows:")
    print(f"\tDescription: {payload['attributes']['interfaceDesc']}")
    print(f"\tname: {payload['attributes']['name']}")
    print(f"\tSecurity Level: {payload['attributes']['securityLevel']}")
    print(f"\tIPv4 Address: {payload['attributes']['ipAddress']['ip']['value']}")
    print(f"\tNetmask: {payload['attributes']['ipAddress']['netMask']['value']}")
    print(f"\tShutdown Status: {payload['attributes']['shutdown']}")
    print("\n")
    payload = payload['attributes'] 
    response = get_response(url, 'patch', username, password, payload)
    print("\n")

def config_keys(payload):
    #This function configures an RSA keypair as defined in payload
    url = f"https://{host}/api/certificate/keypair"
    print(f"Attempting to generate RSA keypair {payload['name']}...")
    response = get_response(url, 'post', username, password, payload)
    print("\n")

def config_cert(payload):
    #This function creates a trustpoint and self-signed cert as defined in paylaod
    url = f"https://{host}/api/certificate/identity"
    print("Attempting to generate self signed certificate...")
    response = get_response(url, 'post', username, password, payload)
    print("\n")

def config_static_route(payload):
    #This function creates a static route as defined in paylaod
    url = f"https://{host}/api/routing/static"
    print("Attempting to configure the following static route...")
    print(f"\tRoute: {payload['network']['value']}")
    print(f"\tNext Hop: {payload['gateway']['value']}")
    print(f"\tOutgoing Interface: {payload['interface']['name']}")
    print("\n")
    response = get_response(url, 'post', username, password, payload)
    print("\n")

def send_cli(payload):
    #This function sends CLI commands as defined in payload, and displays the output of each command
    url = f"https://{host}/api/cli"
    print("Sending the following commands to ASA:")
    for command in payload['commands']:
        print(f"\t{command}")
    response = get_response(url, 'post', username, password, payload)
    print("\n") 
    for cmdoutput in json.loads(response.text)['response']:
        print(cmdoutput)
    print("\n")

def write_config():
    #This function performs a 'wr mem' on the ASA to save configuration
    url = f"https://{host}/api/commands/writemem"
    print("Saving configuration...")
    response = get_response(url, 'post', username, password)
    print("\n")
