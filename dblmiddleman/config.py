from configobj import ConfigObj

class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        
        config = ConfigObj(config_file, interpolation=False, file_error=True)
        
        self.authorization_header = config.get("Options").get("authorization_header")
        self.tasks = config.get("Tasks")
        self.api_token = config.get("Options").get("api_token")