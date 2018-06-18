# Webhook Middleman for Discord Bot List
By EndenDragon

## Description
A configurable receiver of Discord Bots List webhooks. The idea behind the project is to allow the customization that's beyond the original options presented in DBL bot settings. Inside the project, there are plugins that may be utilized to handle out tasks that occurs after receiving a vote notifcation. Feel free to create plugins and suggest them with a pull request. Webhook Middleman is built with Flask to serve the api receiver. This project requires **Python 3.5+**.

## Installation
Use PIP to install packages within `requirements.txt`. The `run.py` and `run_c9.py` (for cloud9) is provided to run the webapp in a development environment. **Do not run these files in production** (unless you want to recreate [Patreon's mistake](https://labs.detectify.com/2015/10/02/how-patreon-got-hacked-publicly-exposed-werkzeug-debugger/)). Follow instructions on [this page](http://flask.pocoo.org/docs/1.0/deploying/#deployment) on deploying a flask website. Then visit the index page to get your webhook options. See the annotated `config.example.ini` on how you should write your `config.ini` file (which you will create at the same location as the example file). The configuration file will be loaded in when the webapp initializes.

## Customizability
This project is created Titan Embeds project in mind. However, I have allowed many custom customization (such as creating your own plugins and configurable options within plugins) to handle an incoming vote webhook. If you would like to add your own plugin, create a file and class (both sharing the same name, with the filename all lowercased). Inside the file, you will need to extend Plugin abstract class. We use jinja2 templating to handle templates in the config. Please see existing plugins to get a sense on how you should create yours. The vote context will be passed in to your `execute` definition when handling a webhook vote.

## Support
Visit our [Titan Embeds support server](http://discord.io/Titan) and talk to EndenDragon regarding to this project.