from django.db import models
from django.template.defaultfilters import lower, slugify
from django.utils.safestring import mark_safe
from datetime import datetime
from radio.managers import ShowManager
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib.sites.models import Site
from django.conf import settings

current_site = Site.objects.get(id=settings.SITE_ID)

class RadioSkin(models.Model):
    """ Holds style & logo information for the player allowing skinning
    and further changes for sponsors """

    CORNER_CHOICES = (
        (0, 'All'),
    )

    name = models.CharField(max_length=255)
    name.help_text = 'Make it descriptive so you can easily refer to it elsewhere!'
    created_at = models.DateTimeField(default=datetime.now())
    prefer = models.BooleanField(default=False)
    prefer.help_text = 'If a skin is preferred the most recently checked one will be used by default'
    radio_logo = models.ImageField(upload_to='uploads/radio/skins/')
    default_banner = models.ImageField(upload_to='uploads/radio/skins/', blank=True, null=True)
    default_banner.help_text = 'Used if there is no current sponsor for a series/show'
    banner_url = models.URLField(blank=True, null=True, verify_exists=False)
    base_background = models.ImageField(upload_to='uploads/radio/skins/', blank=True, null=True)
    base_color = models.CharField(max_length=6, default='000000')
    main_title_color = models.CharField(max_length=6, default='FF0000')
    secondary_title_color = models.CharField(max_length=6, default='FF0000')
    description_color = models.CharField(max_length=6, default='FFFFFF')
    corner_radius = models.IntegerField(default=10)
    rounded_corners = models.IntegerField(choices=CORNER_CHOICES, default=0)
    show_list_color = models.CharField(max_length=6, default='00FF00')
    show_list_limit = models.IntegerField(default=10)
    show_list_limit.help_text = 'Number of shows to list out on the player itself for selection'
    show_list_icon = models.ImageField(upload_to='uploads/radio/skins/', blank=True, null=True)
    embed_icon = models.ImageField(upload_to='uploads/radio/skins/', blank=True, null=True)
    download_icon = models.ImageField(upload_to='uploads/radio/skins/', blank=True, null=True)
    play_show_icon = models.ImageField(upload_to='uploads/radio/skins/', blank=True, null=True)
    flash_config = models.FileField(upload_to='uploads/radio/skins/', blank=True, null=True)
    flash_config.help_text = 'XML file for skinning the flash player'
    css_classes = models.CharField(max_length=255, blank=True, null=True)
    css_classes.help_text = 'Extra class to output on the templatetag divs'
    div_id_prefix = models.CharField(max_length=255, blank=True, null=True)
    div_id_prefix.help_text = 'A prefix to use for the outputted container divs'

    @staticmethod
    def get_active():
        try:
            return RadioSkin.objects.all()[0]
        except IndexError:
            return None


class Sponsor(models.Model):
    """ A sponsor to bind to a show or series to allow outgoing urls &
    banners to be shown as it's playing """

    name = models.CharField(max_length=255)
    player_skin = models.ForeignKey(RadioSkin, null=True, blank=True)
    player_skin.help_text = 'If this sponsor requests full rebranding of the player, add a skin and link it here'
    banner_image = models.ImageField(upload_to='uploads/radio/sponsors/')
    banner_image.help_text = 'Shows on the radio skin as the show or series is being played'
    outgoing_url = models.URLField(blank=True, null=True)
    outgoing_url.help_text = 'The external link to load when clicked'
    description = models.TextField(blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    valid_from.help_text = 'To only allow this sponsor to show during a specific date range specify above'

class Series(models.Model):
    """ Binds to a show to hold common series information. Most can be
    overridden by the show also. """

    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='uploads/radio/series/')
    picture.help_text = 'The main series image, used if you don\'t give a particular show an image'
    description = models.TextField()
    description.verbose_name = 'Series description. If you don\'t update show text this will be used.'
    homepage = models.URLField(blank=True, null=True)
    homepage.help_text = 'A homepage URL for the entire series'
    series_sponsor = models.ForeignKey(Sponsor, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Series'

    def __unicode__(self):
        return '%s' % self.title

class Show(models.Model):
    """ Holds a bunch of show data. You might want to subclass this to use
    a different method of holding media. Both series & sponsor are optional
    so you can have one offs easily. """

    STATUS_CHOICES = (
        (0, 'Offline'),
        (3, 'Upcoming'),
        (5, 'Live'),
    )

    title = models.CharField(max_length=255, blank=True, null=True)
    title.help_text = 'If you need to tweak the series title for this show do it here'
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    subtitle.help_text = 'Want something extra under the main series title?'
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at.help_text = 'Shows are selected based on this date, it will always take the latest 4. If you want to re-order a show change this date.'
    go_live = models.DateTimeField(blank=True, null=True)
    go_live.help_text = 'Allows you to line up a show for a future date'
    description = models.TextField(blank=True, null=True)
    description.verbose_name = 'Show description'
    description.help_text = ''
    picture = models.ImageField(upload_to='uploads/radio/show/', blank=True, null=True)
    media_url = models.URLField(verify_exists=False, blank=True, null=True)
    media_url.help_text = 'If the file is located at an external URL enter it here'
    media = models.FileField(upload_to='uploads/radio/mp3/', blank=True, null=True)
    media.help_text = 'If you are hosting the file on this server (or however the model defines its storage backend) upload it here.'
    show_sponsor = models.ForeignKey(Sponsor, blank=True, null=True)
    series = models.ForeignKey(Series, blank=True, null=True)
    allow_download = models.BooleanField(default=True)
    allow_embed = models.BooleanField(default=True)
    more_info_url = models.URLField(blank=True, null=True)
    more_info_url.help_text = 'If this show has some more information available somewhere else, link it here.'

    objects = models.Manager()
    live = ShowManager()

    def __unicode__(self):
        return '%s' % self.title

    @staticmethod
    def get_latest():
        try:
            return Show.live.all()[0]
        except IndexError:
            return None

    @property
    def live_description(self):
        if self.description:
            return self.description
        elif self.series:
            return self.series.description
        else:
            return None

    @property
    def live_picture(self):
        if self.picture:
            return self.picture.url
        elif self.series:
            return self.series.picture.url
        else:
            return None

    def json_data(self):
        """ Returns the show as a json array for pulling in via jQuery """
        data = {
            'title': self.title,
            'series_title': None,
            'subtitle': self.subtitle,
            'description': self.description,
            'picture': self.live_picture,
            'media': None,
            'flash_player_url': reverse('radio:play', kwargs={'object_id': self.pk}),
            'embed_url': reverse('radio:embed', kwargs={'object_id': self.pk}),
            'download_url': reverse('radio:download', kwargs={'object_id': self.pk}),
        }
        if self.media:
            data.update(dict(media=self.media.url))
        if self.series:
            data.update(dict(series_title=self.series.title))
        return mark_safe(simplejson.dumps(data))

    @models.permalink
    def get_absolute_url(self):
        return ('radio:play', (), {'object_id': self.pk})

    @property
    def short_title(self):
        if self.title:
            return self.title
        elif self.series:
            return self.series.title
        elif self.subtitle:
            return self.subtitle
        else:
            return ''

    @property
    def full_title(self):
        if self.series:
            if self.title:
                return '%s - %s' % (self.series.title, self.title)
            elif self.subtitle:
                return '%s - %s' % (self.series.title, self.subtitle)
        elif self.title:
            if self.subtitle:
                return '%s - %s' % (self.title, self.subtitle)
            else:
                return self.title
        elif self.subtitle:
            return self.subtitle
        else:
            return ''

    @property
    def embed_info(self):
        return '<p><strong>%s</strong></p><p>%s</p>' % (self.full_title, self.live_description)

    @property
    def absolute_media_url(self):
        if self.media:
            return self.media.url
        if self.media_url:
            return self.media_url
        return None

    @property
    def zipped_url(self):
        """ Just drops the mp3 extension for a zip one (for now)"""
        path = self.absolute_media_url
        return path[:-3]+'zip'

    @property
    def flash_player(self):
        file_url = self.absolute_media_url
        if file_url:
            return mark_safe("""
            <object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="250" height="20" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab">
                <param name="movie" value="http://%(base_url)s/media/swf/singlemp3player.swf?file=%(media)s&amp;autoStart=false&amp;backColor=000000&amp;frontColor=ffffff&amp;songVolume=90" />
                <param name="wmode" value="transparent" />
                <embed wmode="transparent" width="250" height="20" src="http://%(base_url)s/media/swf/singlemp3player.swf?file=%(media)s&amp;autoStart=false&amp;backColor=000000&amp;frontColor=ffffff&amp;songVolume=90" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" /></embed>
            </object>
            """ % {'media': file_url, 'base_url': current_site.domain})
        else:
            return ''

    @property
    def embed_code(self):
        skin = RadioSkin.get_active()
        player_code = self.flash_player
        output = """<!-- Start Radio Embed --><table cellspacing="0" cellpadding="0" width="250">
            <tr><td height="30"><a href="http://%(base_url)s" target="_blank"><img src="http://%(base_url)s%(logo)s" alt="Embedded from SpineTV" width="100" border="0" /></a></td>
            <td valign="middle"><a style="font-family:Verdana; font-size:10px; font-weight:bold; text-decoration:none; color:#000;" href="http://%(base_url)s" target="_blank">Find out more at SpineTV</a></td>
            </tr><tr><td colspan="2" style="padding-top:10px;">%(player)s</td></tr>
            <tr><td colspan="2" style="padding-top:10px; font-size:10px; font-family:Verdana;">%(info)s</td></tr>
            </table><!-- End Radio Embed -->""" % {
                'player': player_code,
                'base_url': current_site.domain,
                'logo': skin.radio_logo.url,
                'info': self.embed_info,
            }
        return output.strip()
