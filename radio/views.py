from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils import simplejson as json
from radio.models import Show

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
    return render_to_response('radio/embed.html', context_instance=RequestContext(request))

def download(request, object_id):
    show = get_object_or_404(Show, pk=object_id)
    return render_to_response('radio/download.html', context_instance=RequestContext(request))
