from . import Plugin
from jinja2 import Template

class ConsolePrint(Plugin):
    def __init__(self, *, config):
        self.content_tmpl = Template(config.get("content", ""))
    
    def execute(self, vote):
        rendered = self.content_tmpl.render(vote.__dict__)
        print(rendered)