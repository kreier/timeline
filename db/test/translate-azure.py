# -*- coding: utf-8 -*-

# This simple app uses the '/translate' resource to translate text from
# one language to another.

# You may need to install requests and uuid.
# Run: pip install requests uuid
# From: https://github.com/MicrosoftTranslator/Text-Translation-API-V3-Python

import os, requests, uuid, json

# use this if you want to use environment variables:
# from dotenv import load_dotenv
# load_dotenv()

# key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
# if not key_var_name in os.environ:
#     raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
# subscription_key = os.environ[key_var_name]

# region_var_name = 'TRANSLATOR_TEXT_REGION'
# if not region_var_name in os.environ:
#     raise Exception('Please set/export the environment variable: {}'.format(region_var_name))
# region = os.environ[region_var_name]

# endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
# if not endpoint_var_name in os.environ:
#     raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
# endpoint = os.environ[endpoint_var_name]

# or shorter:

subscription_key = 'e87e0ed07a914b4c9fe6f1d31c122104'
region = 'southeastasia'
endpoint = 'https://api.cognitive.microsofttranslator.com/'

# If you encounter any issues with the base_url or path, make sure
# that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate
path = '/translate?api-version=3.0'
params = '&from=en&to=de&to=yue&to=zh-Hans'
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': region,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# You can pass more than one object in body.
body = [{
    'text' : 'Hello World!'
}]
request = requests.post(constructed_url, headers=headers, json=body)
response = request.json()

print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': ')))
