from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import (
    ProfileDetailView, ProfileUpdateView, ProfileRedirectView
)


urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^redirect/$', ProfileRedirectView.as_view(), name='redirect'),    
    url(r'^(?P<slug>[-\w]+)/$', ProfileDetailView.as_view(), name='profile_detail'),
    url(r'^(?P<slug>[-\w]+)/update/$', ProfileUpdateView.as_view(), name='profile_update'),
]
