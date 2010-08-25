from django.conf.urls.defaults import patterns
from radio.views import *

urlpatterns = patterns('radio.views',
    (r'^json/$', 'showdump', {}, 'json'),
    (r'^$', 'player', {}, 'player'),
)

