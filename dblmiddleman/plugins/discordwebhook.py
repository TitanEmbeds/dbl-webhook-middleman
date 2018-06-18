from . import Plugin
from datetime import datetime
from jinja2 import Template
import json
import requests

class DiscordWebhook(Plugin):
    def __init__(self, *, config):
        self.url = config["url"]
        self.username = config.get("username")
        self.avatar_url = config.get("avatar_url")
        self.content = config.get("content")
        
        if "Embed" in config:
            self.embed = RichEmbed(data=config.get("Embed"))
        
        if self.username:
            self.username_tmpl = Template(self.username)
        if self.avatar_url:
            self.avatar_url_tmpl = Template(self.avatar_url)
        if self.content:
            self.content_tmpl = Template(self.content)
    
    def execute(self, vote):
        headers = {"Content-Type": "application/json"}
        payload = self.to_dict(vote.__dict__)
        requests.post(self.url, headers=headers, data=json.dumps(payload))

    def to_dict(self, vote):
        result = {}
        if self.username:
            result["username"] = self.username_tmpl.render(vote)
        if self.avatar_url:
            result["avatar_url"] = self.avatar_url_tmpl.render(vote)
        if self.content:
            result["content"] = self.content_tmpl.render(vote)
        
        if self.embed:
            result["embeds"] = [self.embed.to_dict(vote)]
        return result

class RichEmbed:
    def __init__(self, *, data):
        self.title = data.get("title")
        self.description = data.get("description")
        self.url = data.get("url")
        self.timestamp = data.get("timestamp")
        self.color = data.get("color")
        
        if "Footer" in data:
            self.footer = RichEmbedFooter(data=data.get("Footer"))
        else:
            self.footer = None
        
        if "Image" in data:
            self.image = RichEmbedPicture(data=data.get("Image"))
        else:
            self.image = None
        
        if "Thumbnail" in data:
            self.thumbnail = RichEmbedPicture(data=data.get("Thumbnail"))
        else:
            self.thumbnail = None
        
        if "Author" in data:
            self.author = RichEmbedAuthor(data=data.get("Author"))
        else:
            self.author = None
        
        self.fields = []
        for key, val in data.items():
            if key.lower().startswith("field"):
                self.fields.append(RichEmbedField(data=val))
        
        if self.title:
            self.title_tmpl = Template(self.title)
        if self.description:
            self.description_tmpl = Template(self.description)
        if self.url:
            self.url_tmpl = Template(self.url)
        if self.timestamp:
            self.timestamp_tmpl = Template(self.timestamp)
        
        if self.color:
            if self.color.startswith("x"):
                self.color = int(self.color[1:], 16)
            else:
                self.color = int(self.color)
    
    def to_dict(self, vote):
        result = {}
        if self.title:
            result["title"] = self.title_tmpl.render(vote)
        if self.description:
            result["description"] = self.description_tmpl.render(vote)
        if self.url:
            result["url"] = self.url_tmpl.render(vote)
        if self.timestamp:
            combined = {**vote, **{"datetime_now": datetime.utcnow().isoformat()}}
            result["timestamp"] = self.timestamp_tmpl.render(combined)
            
        if self.color:
            result["color"] = self.color
            
        if self.footer:
            result["footer"] = self.footer.to_dict(vote)
        if self.image:
            result["image"] = self.image.to_dict(vote)
        if self.thumbnail:
            result["thumbnail"] = self.thumbnail.to_dict(vote)
        if self.author:
            result["author"] = self.author.to_dict(vote)
        
        if self.fields:
            fields = []
            for field in self.fields:
                fields.append(field.to_dict(vote))
            result["fields"] = fields
            
        return result

class RichEmbedFooter:
    def __init__(self, *, data):
        self.text = data.get("text")
        self.icon_url = data.get("icon_url")
        
        if self.text:
            self.text_tmpl = Template(self.text)
        if self.icon_url:
            self.icon_url_tmpl = Template(self.icon_url)
    
    def to_dict(self, vote):
        result = {}
        if self.text:
            result["text"] = self.text_tmpl.render(vote)
        if self.icon_url:
            result["icon_url"] = self.icon_url_tmpl.render(vote)
        return result

# For Image and Thumbnail
class RichEmbedPicture:
    def __init__(self, *, data):
        self.url = data.get("url")
        
        if self.url:
            self.url_tmpl = Template(self.url)
            
    def to_dict(self, vote):
        result = {}
        if self.url:
            result["url"] = self.url_tmpl.render(vote)
        return result

class RichEmbedAuthor:
    def __init__(self, *, data):
        self.name = data.get("name")
        self.url = data.get("url")
        self.icon_url = data.get("icon_url")
        
        if self.name:
            self.name_tmpl = Template(self.name)
        if self.url:
            self.url_tmpl = Template(self.url)
        if self.icon_url:
            self.icon_url_tmpl = Template(self.icon_url)

    def to_dict(self, vote):
        result = {}
        if self.name:
            result["name"] = self.name_tmpl.render(vote)
        if self.url:
            result["url"] = self.url_tmpl.render(vote)
        if self.icon_url:
            result["icon_url"] = self.icon_url_tmpl.render(vote)
        return result
        
class RichEmbedField:
    def __init__(self, *, data):
        self.name = data.get("name")
        self.value = data.get("value")
        self.inline = data.get("inline")
        
        if "inline" in data:
            self.inline = data.as_bool("inline")
        
        if self.name:
            self.name_tmpl = Template(self.name)
        if self.value:
            self.value_tmpl = Template(self.value)
        
    def to_dict(self, vote):
        result = {}
        if self.name:
            result["name"] = self.name_tmpl.render(vote)
        if self.value:
            result["value"] = self.value_tmpl.render(vote)
            
        if self.inline:
            result["inline"] = self.inline
        return result