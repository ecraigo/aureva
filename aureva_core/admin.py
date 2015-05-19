from django.contrib import admin
from aureva_core.models import UserProfile, Genre, Subgenre, Track, Release, Review


class TrackAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.
admin.site.register(Genre)
admin.site.register(Subgenre)
admin.site.register(Track, TrackAdmin)
admin.site.register(Release)
admin.site.register(UserProfile)
admin.site.register(Review)