# This is for creating form classes for all the possible forms on the website. This file will eventually be very long.
from django import forms
from aureva_core.models import User, UserProfile, Track

from django.template.defaultfilters import filesizeformat

# Either 'fields' or 'exclude' must explicitly be specified


class UserForm(forms.ModelForm):  # ModelForm automatically generates a form from a model
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    # This is not rendered but we need to group it with the hidden fields to ensure that it is not.
    links = forms.CharField(widget=forms.HiddenInput(), help_text='A place to show off your spaces on other websites. '
                                                                  'Up to 7 links permitted.', required=False)

    # Supposedly this method is automatically called when the .is_valid() method is called on this form.
    def clean_profile_image(self):

        # Internal settings for this form only.
        profile_picture_types = ['image/gif', 'image/jpeg', 'image/png']
        profile_picture_max_size = 4000000

        file = self.cleaned_data['profile_image']

        if file:
            mime_type = file.content_type

            # No-extension files are not allowed.
            if len(file.name.split('.')) == 1:
                raise forms.ValidationError('This file type is not supported.')

            if mime_type in profile_picture_types:
                if file._size > profile_picture_max_size:
                    raise forms.ValidationError('Only files up to {0} are permitted.'.format(
                        filesizeformat(profile_picture_max_size)
                    ))
            else:
                raise forms.ValidationError('This file type, {0}, is not supported.'.format(mime_type))

    class Meta:
        model = UserProfile
        fields = ['tagline', 'biography', 'location', 'profile_image', 'links']


class TrackForm(forms.ModelForm):
    # This is not rendered but we need to group it with the hidden fields to ensure that it is not.
    tags = forms.CharField(widget=forms.HiddenInput(), help_text='Keywords that relate to your track. These help '
                                                                 'interested users discover it. Up to 7 tags '
                                                                 'permitted.', required=False)

    class Meta:
        model = Track
        fields = ['title', 'genres', 'short_desc', 'long_desc', 'public', 'release', 'tags', 'file']