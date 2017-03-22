from django.apps import AppConfig
from watson import search as watson


class FacemashConfig(AppConfig):
    name = 'girls_proj.facemash'
    verbose_name = 'Facemash'

    def ready(self):
        Facemash = self.get_model("Facemash")
        watson.register(Facemash, fields=("vk_id",),)
