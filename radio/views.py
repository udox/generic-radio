from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils import simplejson as json
from radio.models import Show, PodcastSeries

def showdump(request):
    """ Dumps out the show data as a JSON array for loading into other
    programs (flash maybe? :) """

    return_data = list()
    shows = Show.live.all()[:10]
    for show in shows:
        return_data.append({
            'pk': show.pk,
            'media': show.media.url,
            'image': 'img/shows/active-%s.png' % show.picture,
            'title': show.title,
            'description': show.description,
            'created': show.created_at.strftime('%d/%m/%y %H:%M'),
        })
    return HttpResponse(json.dumps(dict(shows=return_data)))

def player(request):
    return render_to_response('debug.html', context_instance=RequestContext(request))

def embed(request, object_id):
    show = get_object_or_404(Show, pk=object_id)
    return HttpResponse(show.embed_code)

def download(request, object_id):
    show = get_object_or_404(Show, pk=object_id)
    return HttpResponseRedirect(show.zipped_url)

def play(request, object_id):
    show = get_object_or_404(Show, pk=object_id)
    if show.media:
        return HttpResponse(json.dumps(dict(show=show.media.url)), mimetype='application/json')
    else:
        raise Http404

def get_bare_player(request, object_id):
    show = get_object_or_404(Show, pk=object_id)
    if show.media or show.media_url:
        return HttpResponse(show.flash_player)
    else:
        raise Http404

def podcast_xml(request, slug):
    podcast = get_object_or_404(PodcastSeries, url=slug)
    return render_to_response('radio/podcast.xml', {'podcast': podcast},
        mimetype='text/xml')
