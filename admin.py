from music.models import Song, Album
from django.contrib import admin

class SongInline(admin.TabularInline):
    model = Song
    extra = 0

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'album_artist')
    inlines = [SongInline]

class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'album')

admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)
