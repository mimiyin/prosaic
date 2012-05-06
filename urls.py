from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prosaic.views.home', name='home'),
    # url(r'^prosaic/', include('prosaic.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^$', redirect_to, {'url': '/words/'}), # Intercept the CMS page and redirect to welcome
     url(r'^admin/', include(admin.site.urls)), 
     url(r'^words/', include('words.urls'))    
)
