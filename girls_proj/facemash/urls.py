from django.conf.urls import url

from .views import (
    PlayView, RatingsListView, GirlDetailView, FacemashUpdateView
)


urlpatterns = [
    url(r'^$', PlayView.as_view(), name='play'),
    url(r'^ratings/$', RatingsListView.as_view(), name='ratings'),
    url(r'^update/$', FacemashUpdateView.as_view(), name='update'),
    url(r'^g/(?P<slug>[-\w]+)/$', GirlDetailView.as_view(), name='detail'),
]
