from django.conf.urls.defaults import *

urlpatterns = patterns('music.views',
    (r'^$', 'index'),
    (r'^song/(?P<song_id>\d+)/?$', 'song'),
    (r'^reload/?$', 'reload'),
)
