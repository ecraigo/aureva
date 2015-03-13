from django.db import models
from django.contrib.auth.models import User


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
                                                               'to 8 links permitted.')  # JSON, separately displayed
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True, help_text='Must be in .jpg, '
                                      '.png, or .gif formats. Files up to 4 MB are allowed.')

    def __str__(self):
        return self.user.username


class Release(models.Model):
    name = models.CharField(max_length=300)
    artists = models.ManyToManyField(User)

    def __str__(self):
        return self.name + ', by ' + ', '.join(artist.username for artist in self.artists.all())


class Track(models.Model):
    title = models.CharField(max_length=300, help_text='Up to 300 characters.')
    user = models.ForeignKey(User)
    genres = models.ManyToManyField('Subgenre')
    short_desc = models.CharField(blank=True, default='', max_length=160, verbose_name='Short description',
                                  help_text='A quick overview of your track. Up to 160 characters permitted.')
    long_desc = models.TextField(blank=True, default='', verbose_name='Long description', help_text='More track info.')
    public = models.BooleanField(default=True, help_text='Privacy settings. A track that is public is visible from '
                                                         'your profile, while a private track can only be seen by '
                                                         'those with the link.')
    release = models.ForeignKey('Release', blank=True, null=True)
    tags = models.TextField(blank=True, default='')  # JSON, separate display
    file = models.FileField(upload_to='tracks', null=True, help_text='')

    def __str__(self):
        return self.title + ', by ' + self.user.username


class Review(models.Model):
    track = models.ForeignKey('Track')
    user = models.ForeignKey(User)
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)  # NB: This is the rating others have given of the review, not the rating
                                             # the reviewer gave the track.

    def __str__(self):
        return 'Review {0} by {1} on the track {2}'.format(self.id, self.user.username, self.track.name)


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