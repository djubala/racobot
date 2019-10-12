import requests as r
import json


#response = r.get('https://api.fib.upc.edu/v2/o/authorize',headers={'accept': 'application/json'})
params = dict(
    client_id = 'KJ0fFNkeNeTRDKOLRFhsI5nW67w0tZItlgP8909',
    response_type = 'code',
    scope = 'read',
    state = 'random_state_string',
    approval_prompt = 'auto'
)
response = r.get('https://api.fib.upc.edu/v2/o/authorize?',headers={'accept': 'application/json'},params=params)
print(response.content)
#
#fib = oauth.remote_app(
#    'fib',
#    request_token_params={'scope': 'read', 'state': state},
#    base_url=app_url,
#    request_token_url=None,
#    access_token_method='POST',
#    access_token_url=app_url + 'o/token/',
#    authorize_url=app_url + 'o/authorize/',
#    app_key='RACO'
#)
#token_key = 'api_token'
#
#
#def get_urls():
#return fib.get('', headers={'Accept': 'application/json'}).data
