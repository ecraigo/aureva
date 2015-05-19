# Define custom fields such as JSON and specific types of file uploads here.
# There is a much greater degree of control you get with custom fields.

from django import forms
from django.db import models
from Aureva import settings
from django.template.defaultfilters import filesizeformat


# For track uploads.
class AudioField(models.FileField):

    def clean(self, *args, **kwargs):
        data = super(AudioField, self).clean(*args, **kwargs)

        # For a file that has not been changed/uploaded there will be no content_type attribute, triggering
        # AttributeError. This is why we catch this with try/except and go on
        try:
            file = data.file
            content_type = file.content_type

            # Check to see if right MIME type, then check to see file isn't too big
            if content_type in settings.TRACK_FILE_TYPES:

                if file._size > settings.TRACK_MAX_SIZE:
                    raise forms.ValidationError('The maximum file size permitted is {0}. This file is {1}. Please upload a '
                                                'smaller file.'.format(filesizeformat(settings.TRACK_MAX_SIZE),
                                                                       filesizeformat(file._size)))

            else:
                raise forms.ValidationError('This file type, {0}, is not in the list of allowed file types for tracks. Please '
                                            'upload a different file type.'.format(content_type))
        except AttributeError:
            pass

        return data


# For lists and other more complex structures.
class JSONField(forms.Field):
    pass