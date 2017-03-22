from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import (
    SearchListView, AboutPage
)


urlpatterns = [
    url(r'^about/$', AboutPage.as_view(), name='about'),
    url(r'^search/$', SearchListView.as_view(), name='search'),
]

