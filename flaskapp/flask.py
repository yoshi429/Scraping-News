import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ScrapingProject.settings")
from django.apps import apps
from django.conf import settings
apps.populate(settings.INSTALLED_APPS)

from flask import Flask
from flaskapp.scraping.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

app = create_app()

from flaskapp.scraping import routes