from dblmiddleman.enums import VoteType
from dblmiddleman.restapi import RestApi
from dblmiddleman.user import User
import abc
import importlib

class Plugin(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, *, config):
        raise NotImplementedError
    
    @abc.abstractmethod
    def execute(self, vote):
        raise NotImplementedError
        
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Plugin:
            mro = C.__mro__
            for attr in ("__init__", "execute"):
                for base in mro:
                    if attr in base.__dict__:
                        break
                else:
                    return NotImplemented
            return True
        return NotImplemented
        
class SuperPlugin(Plugin):
    def __init__(self, *, config, api_token):
        self.restapi = RestApi(api_token)
        self.tasks = config
        self.tasks_store = {}
        self.used_plugins = {}
        
        for bot_id, bot_tasks in self.tasks.items():
            self.tasks_store[bot_id] = []
            for task_name, single_task in bot_tasks.items():
                plugin_name = single_task["plugin"]
                plugin = self.get_plugin(plugin_name)
                initialized_plugin = plugin(config=single_task)
                if single_task.get("no_test", None) == None:
                    single_task["no_test"] = "False"
                self.tasks_store[bot_id].append({
                    "plugin": initialized_plugin,
                    "no_test": single_task.as_bool("no_test")
                })
    
    def get_plugin(self, plugin_name):
        if plugin_name in self.used_plugins:
            return self.used_plugins[plugin_name]
        module = importlib.import_module("dblmiddleman.plugins." + plugin_name.lower())
        plugin = getattr(module, plugin_name)
        self.used_plugins[plugin_name] = plugin
        return plugin
    
    def execute(self, vote):
        if isinstance(vote.user, str):
            vote.user = self.restapi.get_user(vote.user)
        tasks = self.tasks_store.get(vote.bot, [])
        for task in tasks:
            if vote.type is VoteType.test and task["no_test"]:
                continue
            task["plugin"].execute(vote)