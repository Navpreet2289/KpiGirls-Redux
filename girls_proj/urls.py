from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^', include('girls_proj.facemash.urls', namespace='facemash')),
    url(r'^', include('girls_proj.landing.urls', namespace='landing')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^accounts/', include('girls_proj.accounts.urls', namespace='accounts')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
