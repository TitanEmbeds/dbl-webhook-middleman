from flask import Flask, abort, request, url_for
from .config import Config
from .plugins import SuperPlugin
from .vote import Vote

app = Flask(__name__)
config = Config("config.ini")
super_plugin = SuperPlugin(config=config.tasks, api_token=config.api_token)

@app.route("/")
def index_endpoint():
    url = url_for(".webhook_endpoint", _external=True)
    return "Use <pre><code>{0}</code></pre> for Discord Bots List webhook URL".format(url)

@app.route("/webhook-endpoint", methods=["POST"])
def webhook_endpoint():
    if request.headers.get("Authorization", "") != config.authorization_header:
        abort(403)
    incoming = request.get_json()
    if not incoming:
        incoming = {}
    required_keys = ["bot", "user", "type"]
    if not all(elem in incoming.keys()  for elem in required_keys):
        abort(400)
    vote = Vote(data=incoming)
    super_plugin.execute(vote)
    return ("", 204);