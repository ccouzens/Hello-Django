from django.db import models
from django.core.urlresolvers import reverse

class Album(models.Model):
    title = models.CharField(
        max_length=100)

    album_artist = models.CharField(
        max_length=100,
        blank=True)

    def __unicode__(self):
        return self.title


from mutagen.mp4 import MP4
class Song(models.Model):
    file_name = models.FilePathField(
        path="/home/chris/Music/",
        match="\.m4a$",
        recursive=True)

    title = models.CharField(
        max_length=100,
        blank=True)

    disc = models.SmallIntegerField(
        null=True)

    track_number = models.SmallIntegerField(
        null=True)

    album = models.ForeignKey(
        Album,
        null=True)

    def __unicode__(self):
        return self.title or self.file_name

    def read_metadata_from_file(self):
        audio = MP4(self.file_name)
        self.title = audio["\xa9nam"][0]
        if self.title=='Arizona' and False:
            print audio.pprint()
            print "----------------------------------------"
            print
            print audio.keys()

        self.track_number = audio["trkn"][0][0]
        try:
            self.disc = audio["disk"][0][0]
        except KeyError:
            self.disc = 1

        album_artist = (audio.get('aART') or audio.get('\xa9ART'))[0]
        album_title = audio.get('\xa9alb')[0]
        try:
            album = Album.objects.get(title=album_title, album_artist=album_artist)
        except Album.DoesNotExist:
            album = Album(title=album_title, album_artist=album_artist)
            album.save()
        self.album = album

    @models.permalink
    def get_absolute_url(self):
        return ('music.views.song', [str(self.id)])

