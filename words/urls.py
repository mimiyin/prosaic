from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('words.views',
    url(r'^$', 'index'),
    url(r'^queue/$', 'queue', name='queue'),
    url(r'^controls/$', 'controls', name='controls'),
)