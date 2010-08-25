from django.contrib import admin
from radio.models import Show, Sponsor, Series, RadioSkin

class RadioAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'media', 'status',)
    list_filter = ('title', 'created_at', 'status', )

    fieldsets = (
        ('Show Information', {'fields': ('title', 'series', 'subtitle',
            'description', 'picture', 'more_info_url')}),
        ('Status & Dates', {'fields': ('status', 'go_live',)}),
        ('Media', {'fields': ('media',)}),
        ('Sponsoring', {'fields': ('show_sponsor',)}),
        ('Options', {'fields': ('allow_download', 'allow_embed')}),
    )

class SkinAdmin(admin.ModelAdmin):
    list_display = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'prefer', 'created_at')}),
        ('Base Skin', {'fields': ('radio_logo', 'default_banner', 'banner_url',
            'base_background', 'base_color', 'main_title_color', 'description_color',
            'show_list_color',)
        }),
        ('Icons', {'fields': ('embed_icon', 'download_icon', 'play_show_icon',
            'show_list_icon')}),
        ('Extras', {'fields': ('corner_radius', 'rounded_corners')}),
        ('Flash Player Config', {'fields': ('flash_config',)}),
        ('Advanced', {'fields': ('css_classes', 'div_id_prefix')}),
    )

class SponsorAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Media & Linking', {'fields': ('player_skin', 'banner_image',
            'outgoing_url')}),
        ('Validity', {'fields': ('valid_from', 'valid_to')}),
    )

class SeriesAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'description', 'homepage', 'picture')}),
        ('Sponsoring', {'fields': ('series_sponsor',)}),
    )

admin.site.register(Show, RadioAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(RadioSkin, SkinAdmin)
