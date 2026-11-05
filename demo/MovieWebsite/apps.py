from django.apps import AppConfig


class MoviewebsiteConfig(AppConfig):
    name = 'MovieWebsite'

    def ready(self):
        from . import signals 