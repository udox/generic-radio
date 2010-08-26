from django.conf.urls.defaults import patterns
from radio.views import *

urlpatterns = patterns('radio.views',
    # We add seperate paths for embeds & downloads to track more easily
    # the media accesses
    (r'^embed/(?P<object_id>\d+)/$', 'embed', {}, 'embed'),
    (r'^download/(?P<object_id>\d+)/$', 'download', {}, 'download'),

    # Used to dump out full data for 3rd party apps
    (r'^json/$', 'showdump', {}, 'json'),

    # Our actual player standalone
    (r'^$', 'player', {}, 'player'),
)
