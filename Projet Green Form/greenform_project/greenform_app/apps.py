from django.apps import AppConfig


# class GreenformAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'greenform_app'


class GroupConfig(AppConfig):
    name='greenform_app'
    def ready(self):
        import greenform_app.signals