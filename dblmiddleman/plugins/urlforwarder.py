from . import Plugin
import json
import requests

class UrlForwarder(Plugin):
    def __init__(self, *, config):
        self.url = config["url"]
        self.authorization_header = config.get("authorization_header")
    
    def execute(self, vote):
        headers = {
            "Content-Type": "application/json"
        }
        if self.authorization_header:
            headers["Authorization"] = self.authorization_header
        payload = {
            "bot": vote.bot,
            "user": vote.user.id,
            "type": str(vote.type)
        }
        
        if vote.query:
            payload["query"] = vote.query
        
        requests.post(self.url, headers=headers, data=json.dumps(payload))