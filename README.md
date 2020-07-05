Interact with Cisco ASA via ASA REST API

This project provides code to programatically configure certain aspects of a Cisco ASA firewall using Python and the ASA REST API. This code was written and tested with Python 3.8, and ASA 9.14(1) with version 7.14.1 of the ASA REST API Plugin.

Getting Started:

- Download and configure the ASA REST API plugin from Cisco: https://www.cisco.com/c/en/us/td/docs/security/asa/api/qsg-asa-api.html
- Make sure you can access the API documentation at https://<ASA_IP>/doc
- Edit device.json for your specific deployment details
- Run config_asa.py to configure your ASA

About asa_module.py:

This python module contains all the functions related to interacting with ASA via REST API. The following functions exist so far:
   - init_params(params) - Initializes global variables used in all other API calls (like username, password, host)
   - get_response(url, method, username, password, payload='') - Generic function implementing the actual HTTP API calls using requests module
   
   - get_interfaces(): Retrieves and prints certain information about physical interfaces
   - enable_dns(payload): Enables DNS lookups on a specified interface
   - config_dns(payload): Modifies an *existing* DNS server group defined in the payload
   - config_ntp(payload): Configures new NTP servers as defined in the payload
   - config_interface(payload): Modifies the configuration of an *existing* physical interface as defined in the payload
   - config_keys(payload): Creates a new RSA keypair as defined in the payload
   - config_cert(payload): Creates a new trustpoint and a self-signed certificate as defined in the payload.
   - config_static_route(payload): Creates a new static route as defined in the payload
   - send_cli(payload): Sends CLI commands to the ASA, and prints the output of each command sent
   - write_config(): Saves the running-configuration to startup-configuration
   
About device.json:

This is a JSON file containing all the specific information about your ASA device, and the configuration payloads that will be sent (in order).
   - host - The FQDN or IP address of your ASA
   - username - Username used to interact with the API
   - password - Password used to interact with the API
   - Attributes - This is an array (list) of JSON objects (dictionaries), where each object is an attribute on ASA you wish to configure
      - name: Name of the attribute
      - description: A friendly description of the information this attribute holds
      - execute: Boolean value.  If set to true, this attribute will be processed. Otherwise, it won't be processed (by config_asa.py)
      - execute_function: The specific function that will be called from config_asa.py to actually implement this attribute
      - payloads: An array (list) of payloads.  This will be used in the case where an attribute has multiple payloads you wish to send
      - payload: An object (dictionary) that contains the payload to be sent to the device
     
Ultimately, config_asa.py will open this json file, and loop through each attribute, executing each particular attribute with "execute" set to true.

About config_asa.py:

This is the main Python code that puts everything together. Essentially, it accomplishes the following:
   - Opens device.json, reads and parses it, and stores it as a Python dictionary named device
   - Reads the value of the host, username, and password keys from device, and stores them in a dictionary called params
   - Calls init_params from the ASA module.  This is how global parameters that are necessary get passed into the asa_module.py module 
   - Prompts the user on if they really want to continue with configuration
   - Loops through all attributes in the device dictionary
      - If "execute" is set to true, that attribute is configured.  Otherwise, that attribute is skipped
   - Saves the ASA configuration
   
Please note, if you use config_asa.py as is, the attributes stored in device.json are executed *in order*, so make sure your attributes are set up in device.json in the order you want them executed.  For example, putting the "Identity Certificate" module ahead of the "RSA Keypair" module would cause a failure, because the "Identity Certificate" module relies on the RSA keypair created by "RSA Keypair" module.
