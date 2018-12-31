from .exceptions import HTTPException
from .user import User
import json
import requests
import sys

def json_or_text(response):
    text = response.text
    if "application/json" in response.headers["Content-Type"]:
        return response.json()
    return text

class RestApi:
    def __init__(self, api_token):
        self.endpoint = "https://discordbots.org/api"
        self.user_agent = "DBL Webhook Middleman (https://github.com/TitanEmbeds/dbl-webhook-middleman) Python/{0} requests/{1}".format(sys.version_info, requests.__version__)
        self.api_token = api_token
    
    def request(self, verb, url, **kwargs):
        headers = {
            "User-Agent": self.user_agent,
            "Authorization": self.api_token
        }
        
        params = None
        if "params" in kwargs:
            params = kwargs["params"]
        data = None
        if "data" in kwargs:
            data = kwargs["data"]
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
        data = json.dumps(data)
        
        url_formatted = self.endpoint + url
        req = requests.request(verb, url_formatted, params=params, data=data, headers=headers)
        
        if 300 > req.status_code >= 200:
            return json_or_text(req)
        raise HTTPException(req.status_code, req.text)
    
    def get_user(self, user_id):
        _endpoint = "/users/{0}".format(user_id)
        r = self.request("GET", _endpoint)
        return User(data=r)