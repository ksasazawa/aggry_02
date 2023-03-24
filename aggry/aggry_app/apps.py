from django.apps import AppConfig


class AggryAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aggry_app'
    
    # 追加
    def ready(self):
        # 同じ階層にあるap_scheduler.pyのstart()をimportする
        from .ap_scheduler import start
        start()


from django.apps import AppConfig
