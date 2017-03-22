from girls_proj.facemash.models import Facemash


def check_girl(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        try:
            vk_id = response.get('user_id')
            facemash = Facemash.objects.get(vk_id=vk_id)
            facemash.user = user
            facemash.save()
        except Facemash.DoesNotExist:
            pass
