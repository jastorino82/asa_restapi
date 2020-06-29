import asa_module as asa
import json

with open('device.json') as json_file:
    device = json.load(json_file)

params = {}
params['host'] = device['host']
params['username'] = device['username'] 
params['password'] = device['password'] 

print(f"Attempting to configure {params['host']}...\n")
asa.init_params(params)

for interface in device['interfaces']:
    asa.config_interface(interface)

#asa.get_interfaces()
#asa.send_cli(device['commands'])
asa.config_keys(device['keys'])
asa.config_cert(device['identity_cert'])
#asa.write_config()

for route in device['static_routes']:
    asa.config_static_route(route)
