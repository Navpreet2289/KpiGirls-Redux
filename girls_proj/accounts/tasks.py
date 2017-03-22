from girls_proj.celery import app

from .models import Profile


@app.task()
def test_task():
    u_p = Profile.objects.filter(user__username="user").first()
    u_p.address_line1 = 'Successfully tested Celery'
    u_p.save()
