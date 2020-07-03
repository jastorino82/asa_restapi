#main script to configure ASA device
import asa_module as asa
import json
from time import sleep

print("Reading desired ASA configuration from device.json...")
try:
    with open('device.json') as json_file:
        device = json.load(json_file)
except Exception as e:
    raise SystemExit(e)

params = {}
params['host'] = device['host']
params['username'] = device['username'] 
params['password'] = device['password'] 


print(f"Initializing {params['host']}...\n")
asa.init_params(params)

print(f"ASA {params['host']} will be configured based on the contents of device.json")
while True:
    choice = input("Are you sure you want to continue with configuration? (y/n): ")
    if choice == 'n':
        exit()
    elif choice == 'y':
        break

for attribute in device['attributes']:
    if attribute['execute'] == True:
        print(f"Configuring attribute: {attribute['name']}\n")
        if 'payloads' in attribute.keys():
            for payload in attribute['payloads']:
                #print(json.dumps(payload, indent=4))
                cmd = "asa." + attribute['execute_function']
                eval(cmd)
                sleep(2)
        elif 'payload' in attribute.keys():
            #print(json.dumps(attribute['payload'], indent=4))
            cmd = "asa." + attribute['execute_function']
            eval(cmd)
            sleep(2)

asa.write_config()
