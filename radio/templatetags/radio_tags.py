from django.template import Library
from radio.models import Series, Show, Sponsor, RadioSkin
from django.conf import settings

register = Library()

SHOWLIST_LIMIT = 10
SERIES_LIMIT = 5
RANDOM_SERIES = True
PLAYER_TITLE = 'Spine Radio'
PLAYER_LEADIN = 'New shows every month from...'

# Ok, starting to think should automate the below... #lazycoder
if hasattr(settings, 'RADIO_SHOWLIST_LIMIT'):
    SHOWLIST_LIMIT = settings['RADIO_SHOWLIST_LIMIT']
if hasattr(settings, 'RADIO_SERIES_LIMIT'):
    SERIES_LIMIT = settings['RADIO_SERIES_LIMIT']
if hasattr(settings, 'RADIO_RANDOM_SERIES '):
    RANDOM_SERIES = settings['RADIO_RANDOM_SERIES ']
if hasattr(settings, 'RADIO_PLAYER_TITLE'):
    PLAYER_TITLE = settings['RADIO_PLAYER_TITLE']
if hasattr(settings, 'RADIO_PLAYER_LEADIN'):
    PLAYER_LEADIN = settings['RADIO_PLAYER_LEADIN']

@register.inclusion_tag('radio/player.html')
def radio_player():
    """ Renders out the full player on site """
    shows = Show.live.all()[:SHOWLIST_LIMIT]
    skin = RadioSkin.get_active()
    main_show = Show.get_latest()
    return {
        'shows': shows,
        'skin': skin,
        'main_show': main_show,
    }

@register.inclusion_tag('radio/banner.html')
def radio_banner(player_link=None):
    """ Renders out a banner for linking through to the player """
    series = Series.objects.all()
    if RANDOM_SERIES:
        series = series.order_by('?')
    series = series[:SERIES_LIMIT]
    return {
        'series': series,
        'player_title': PLAYER_TITLE,
        'player_leadin': PLAYER_LEADIN,
        'MEDIA_URL': settings.MEDIA_URL,
    }
