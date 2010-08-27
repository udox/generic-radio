from django.conf.urls.defaults import patterns
from radio.views import *

urlpatterns = patterns('radio.views',
    # We add seperate paths for file actions to track more easily
    # the media accesses and what's being done
    (r'^embed/(?P<object_id>\d+)/$', 'embed', {}, 'embed'),
    (r'^download/(?P<object_id>\d+)/$', 'download', {}, 'download'),
    (r'^play/(?P<object_id>\d+)/$', 'get_bare_player', {}, 'play'),
    (r'^podcast/(?P<slug>[\w-]+)/$', 'podcast_xml', {}, 'podcast'),

    # Used to dump out full data for 3rd party apps
    (r'^json/$', 'showdump', {}, 'json'),

    # Our actual player standalone
    (r'^$', 'player', {}, 'player'),
)
