from django.template import Library
from radio.models import Series, Show, Sponsor, RadioSkin
from django.conf import settings

register = Library()

SHOWLIST_LIMIT = 10
if hasattr(settings, 'RADIO_SHOWLIST_LIMIT'):
    SHOWLIST_LIMIT = settings['RADIO_SHOWLIST_LIMIT']

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

    return {

    }
