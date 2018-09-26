from django.conf import settings
from django.conf.urls import patterns, include, url
from settings import VIRTUAL_DIRECTORY

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^{0}'.format(VIRTUAL_DIRECTORY), include('remapp.urls')),
    url(r'^{0}openrem/'.format(VIRTUAL_DIRECTORY), include('remapp.urls')),
    url(r'^{0}admin/'.format(VIRTUAL_DIRECTORY), include(admin.site.urls)),
    # Login / logout.
    url(r'^{0}login/$'.format(VIRTUAL_DIRECTORY), 'django.contrib.auth.views.login', name='login'),
    url(r'^{0}logout/$'.format(VIRTUAL_DIRECTORY), 'remapp.views.logout_page', name='logout'),

)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^{0}__debug__/'.format(VIRTUAL_DIRECTORY), include(debug_toolbar.urls)),
    ] + urlpatterns
