from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

from music.models import Song, Album
from os import walk
from os.path import splitext, join

def index(request):
    all_song_list = Song.objects.order_by('album', 'disc', 'track_number')
    return render_to_response('music/index.html', {
        'all_song_list': all_song_list,
    },
    context_instance=RequestContext(request))

def albums(request):
    all_album_list = Album.objects.order_by('album_artist', 'title')

def song(request, song_id):
    s = get_object_or_404(Song, pk=song_id)
    fsock = open(s.file_name, 'rb')
    return HttpResponse(fsock, content_type='audio/mp4')

def reload(request):
    if request.method != 'POST':
        return HttpResponseForbidden("Access page through POST only")
    Song.objects.all().delete()
    Album.objects.all().delete()
    for root, dirs, files in walk("/home/chris/Music"):
        for f in (f for f in files if splitext(f)[1] == ".m4a"):
            filename = join(root, f)
            s = Song(file_name = filename)
            s.read_metadata_from_file()
            s.save()

    return HttpResponseRedirect(reverse('music.views.index'))
