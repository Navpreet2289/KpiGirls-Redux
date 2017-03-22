from django.apps import AppConfig
from watson import search as watson


class AccountsConfig(AppConfig):
    name = 'girls_proj.accounts'
    verbose_name = 'Accounts'

    def ready(self):
        Profiles = self.get_model("Profile")
        watson.register(Profiles)
