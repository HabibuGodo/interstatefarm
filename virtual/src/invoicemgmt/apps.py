from django.apps import AppConfig


class InvoicemgmtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'invoicemgmt'

    def ready(self):
        import invoicemgmt.signals
