#main script to configure ASA device
import asa_module as asa
import json
from time import sleep

failure_list = []

#Open JSON file describing operations to perform
print("Reading desired ASA configuration from device.json...")
try:
    with open('device.json') as json_file:
        device = json.load(json_file)
except (FileNotFoundError, OSError) as e:
    print("\nFile not found, please make sure device.json exists")
    raise SystemExit(e)

except json.decoder.JSONDecodeError as e:
    print("\nThere is a problem with the contents of device.json. Please double check syntax of the file")
    raise SystemExit(e)

#Pass global parameters into the ASA module so functions in the module can utlize these variables globally
params = {}
params['host'] = device['host']
params['username'] = device['username'] 
params['password'] = device['password'] 
print(f"Initializing {params['host']}...\n")
asa.init_params(params)

#Prompt user to make sure they want to continue
print(f"ASA {params['host']} will be configured based on the contents of device.json")
while True:
    choice = input("Are you sure you want to continue with configuration? (y/n): ")
    if choice == 'n':
        raise SystemExit() 
    elif choice == 'y':
        break
print("\n\n")

#Cycle through all modules in JSON and execute each as necessary
for module in device['modules']:
    if module['execute'] == True:
        print(f"\nConfiguring module: {module['name']}")
        print(f"Module description: {module['description']}\n")
        #Attempt to execute each payload in the module
        if 'payloads' in module.keys():
            for payload in module['payloads']:
                cmd = "asa." + module['execute_function']
                try:
                    response = eval(cmd)
                    #If the response is from the CLI module
                    if ((response.text) and ('response' in response.json().keys()) 
                            and (len(response.json().keys()) == 1)): 
                        cmdoutputs = response.json()['response']
                        for cmdoutput in cmdoutputs:
                            print(cmdoutput)
                    #Pretty print the JSON response
                    elif response.text:
                        print(json.dumps(response.json(), indent=4) + '\n')

                #Catch exceptions and build a list of dictionaries with details
                except Exception as e:
                    #raise SystemExit(e)
                    failure_dict = {}
                    try:
                        error_response = json.dumps(json.loads(str(e)), indent=4)
                    except ValueError:
                        error_response = e
                    print(error_response)
                    print('\n')
                    failure_dict['Module'] = module['name']
                    failure_dict['Module Description'] = module['description']
                    failure_dict['Payload Description'] = payload['description']
                    failure_dict['Error Response'] = error_response
                    failure_list.append(failure_dict)
                    sleep(.2)
                    continue
                sleep(.2)
print("Done!")
#If there were exceptions, show the details
if failure_list:
    print("The following errors occurred:\n")
    for failure in failure_list:
        for k,v in failure.items():
            print(f"{k}: {v}")
        print("\n\n")

asa.write_config()
