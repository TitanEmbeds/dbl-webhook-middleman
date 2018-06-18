from .enums import VoteType, try_enum
import urllib.parse as urlparse

class Vote:
    def __init__(self, *, data):
        self.bot = data["bot"]
        self.user = data["user"]
        self.type = try_enum(VoteType, data["type"])
        self.query = data.get("query")
    
    @property
    def get_queries(self):
        parsed = urlparse.urlparse(self.query)
        return urlparse.parse_qs(parsed.query)