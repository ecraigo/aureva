from Aureva import settings

from django.db import models
from aureva_core import fields  # Custom fields

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from itertools import count

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from datetime import datetime

# Tasks for Celery
from aureva_core.tasks import generate_waveform

# Create your models here.

# "blank" means it is not a required field, "help_text" displays in forms, "null" means null it when it is created,
# useful except for in string fields


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    level = models.IntegerField(default=1)
    tagline = models.CharField(max_length=160, default='', help_text='A short summary of who you are and what you do.'
                                                                     ' Up to 160 characters permitted.')
    biography = models.TextField(default='', help_text='A place for you to explain a bit more about yourself.')
    location = models.CharField(blank=True, max_length=160, default='')
    links = models.TextField(blank=True, default='', help_text='A place to show off your spaces on other websites. Up '
                                                               'to 7 links permitted.')  # JSON, separately displayed

    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True, help_text='Must be in .jpg, '
                                      '.png, or .gif formats. Files up to 4 MB are allowed.')
    thumb_large = models.ImageField(upload_to='profile_images', blank=True, null=True)  # For displaying in profiles
    thumb_small = models.ImageField(upload_to='profile_images', blank=True, null=True)  # For displaying when logged in on navbar

    def __str__(self):
        return self.user.username

    # Automatically generate thumbnails for profile image when saving
    def save(self, *args, **kwargs):

        self.thumb_large = None
        self.thumb_small = None

        if self.profile_image:

            sizes = {'large': (200, 200),
                     'small': (20, 20)}

            mime_to_pil = {'image/jpeg': ['jpeg', 'jpg'],
                           'image/png': ['png', 'png'],
                           'image/gif': ['gif', 'gif']}

            mime = self.profile_image.file.content_type
            pil_type = mime_to_pil[mime][0]
            extension = mime_to_pil[mime][1]

            # Open this original in Pillow
            image = Image.open(BytesIO(self.profile_image.read()))

            temp_file_objs = {}

            for size in sizes:
                temp_img = image.copy()
                temp_img.thumbnail(sizes[size], Image.ANTIALIAS)  # 'ANTIALIAS' makes for the highest-quality thumbs

                temp_bytes = BytesIO()
                temp_img.save(temp_bytes, pil_type)  # Dump contents into raw bytes
                temp_bytes.seek(0)  # Prepare to read from beginning

                # Make a temporary Django file object to then read into the waveforms' ImageFields
                temp_file_objs[size] = SimpleUploadedFile(os.path.split(self.profile_image.name)[-1],
                                                          temp_bytes.read(), content_type=mime)

            image.close()

            # Finally get into our fields here
            self.thumb_large.save('{0}_thumb_lg.{1}'.format(
                os.path.splitext(temp_file_objs['large'].name)[0], extension),
                temp_file_objs['large'], save=False)
            # save = False here because we don't want to automatically save the whole model

            self.thumb_small.save('{0}_thumb_sm.{1}'.format(
                os.path.splitext(temp_file_objs['small'].name)[0], extension),
                temp_file_objs['small'], save=False)

        # Finally call the parent save method
        super(UserProfile, self).save(*args, **kwargs)


class Release(models.Model):
    name = models.CharField(max_length=300)
    artists = models.ManyToManyField(User)

    def __str__(self):
        return self.name + ', by ' + ', '.join(artist.username for artist in self.artists.all())


class Track(models.Model):
    title = models.CharField(max_length=300, help_text='Up to 300 characters.')
    user = models.ForeignKey(User, related_name='tracks')
    date_uploaded = models.DateTimeField(auto_now_add=True, blank=True)
    genres = models.ManyToManyField('Subgenre')
    short_desc = models.CharField(blank=True, default='', max_length=160, verbose_name='Short description',
                                  help_text='A quick overview of your track. Up to 160 characters permitted.')
    long_desc = models.TextField(blank=True, default='', verbose_name='Long description', help_text='More track info.')
    public = models.BooleanField(default=True, help_text='Privacy settings. A track that is public is visible from '
                                                         'your profile, while a private track can only be seen by '
                                                         'those with the link.')
    release = models.ForeignKey('Release', blank=True, null=True)
    tags = models.TextField(blank=True, default='', help_text='Keywords that relate to your track. These help '
                                                              'interested users discover it. Up to 7 tags '
                                                              'permitted.')  # JSON, separate display

    file = fields.AudioField(upload_to='tracks', null=True, help_text='Must be in mp3, FLAC, wav, ogg, AAC, WebM, or '
                                                                      'mp4 formats. Files up to 100 MB are allowed.')
    slug = models.SlugField(unique=False, max_length=50, default='')
    # Above is for the URL generation, because track names by themselves will not make for secure URLs.

    waveform = models.ImageField(upload_to='waveforms', blank=True, null=True)

    class Meta:
        # So that we display things from most to least recent
        ordering = ['-date_uploaded']

    def __str__(self):
        return self.title + ', by ' + self.user.username

    # Ensure that valid, unique URLs are assigned to each song
    # FIXME: This is a silly non-issue, but right now users cannot make more than 9999999999 tracks with the same name
    # if the track names are 40 characters long or longer
    def save(self, *args, **kwargs):
        self.slug = orig = slugify(self.title[:40] if len(self.title) > 40 else self.title)
        # Only mirror 40 chars as len < 50

        # Ensure that there are numbers inserted afterwards if slug is not found to be unique for this artist.
        for x in count(1):
            if not Track.objects.filter(slug=self.slug, user=self.user):
                break
            self.slug = '{0}-{1}'.format(orig, x)

        # Generating waveforms for use on user pages to link to tracks
        self.file.save(self.file.name, self.file, save=False)
        self.waveform = None
        path_to_track = os.path.join(settings.MEDIA_ROOT, self.file.name)
        task_result = generate_waveform.delay(path_to_track)
        raw_image_data = task_result.get()

        # Make a temporary Django file object to then read into the thumbnails' ImageFields
        temp_file_obj = SimpleUploadedFile(os.path.split(self.file.name)[-1],
                                           raw_image_data, content_type='image/png')

        # Finally store in our field
        self.waveform.save('{0}.png'.format(temp_file_obj.name), temp_file_obj, save=False)

        super(Track, self).save(*args, **kwargs)



class Review(models.Model):
    track = models.ForeignKey('Track')
    user = models.ForeignKey(User)
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)  # NB: This is the rating others have given of the review, not the rating
                                             # the reviewer gave the track.
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Review {0} by {1} on the track {2}'.format(self.id, self.user.username, self.track.name)

    class Meta:
        # So that comments are displayed by date descending by default
        ordering = ['-date']


class Genre(models.Model):
    name = models.CharField(max_length=80)
    desc = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class Subgenre(models.Model):
    name = models.CharField(max_length=80)
    desc = models.TextField(blank=True, default='')
    genre = models.ManyToManyField('Genre')

    def __str__(self):
        return self.name + ", a subgenre of " + ', '.join(genre.name for genre in self.genre.all())


class ReviewRating(models.Model):
    review = models.ForeignKey('Review')
    user = models.ForeignKey(User)
    vote = models.BooleanField(default=True)