# Most fundamental imports
from django.template import RequestContext, loader
from django.shortcuts import render

# Helpers, assistant functions
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Authentication
from aureva_core.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Custom models to be used
from aureva_core.models import Track


# Create your views here.
def index(request):

    template = loader.get_template('aureva_core/splash_page.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def register(request):

    registered = False  # A flag letting us know if user registration was successful

    # If we are submitting information here
    if request.method == 'POST':

        # Grab user & profile forms from the data
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Check to see that both forms have correct data entered in
        if user_form.is_valid() and profile_form.is_valid():

            # Create user and save to the database, simultaneously
            user = user_form.save()

            # We must hash password and re-save
            user.set_password(user)
            user.save()

            # Create profile without committing to the database. We must first link it to the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            # Print any errors to the console, and display to the user
            print(user_form.errors, profile_form.errors)
            messages.error(request, 'There were errors in submitting this form. Please check your input and try again.')

    # Not a POST request? Make blank forms
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'aureva_core/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def login_user(request):

    # Figure out the page we are currently on, so that we can redirect back to it if need be
    redirect_to = request.GET.get('next', '/')
    print(redirect_to)

    # Check if this is a POST request
    if request.method == 'POST':

        # Check if input is empty or not
        if request.POST['username'] and request.POST['password']:

            # Obtain data from the form
            username = request.POST['username']
            password = request.POST['password']

            # Returns a User object if login succeeds, None if login fails
            user = authenticate(username=username, password=password)

            # Validate data now.
            if user:

                # Check that user is not disabled. If active, log him/her in.
                if user.is_active:
                    login(request, user)

                    # Note that these redirects go to HTTP links while the render functions go to actual filenames.
                    return HttpResponseRedirect(redirect_to)

                else:
                    messages.error(request, 'This account is currently disabled. Please login using another account '
                                            'or contact an administrator.')
                    return HttpResponseRedirect(redirect_to)

            else:  # User input found to be incorrect.
                print('Login failed (username = "{0}", password = "{1}").'.format(username, password))
                messages.error(request, 'No account exists with these credentials. Please check your input and try '
                                        'again.')
                return HttpResponseRedirect(redirect_to)

        else:  # No input in one or both of the two boxes.
            messages.error(request, 'Please fill out both fields and try again.')
            return HttpResponseRedirect(redirect_to)

    else:  # Not POST? Return bad request
        raise SuspiciousOperation()


# Only those who are logged in should be able to access this view.
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/aureva/')


def user_profile(request, username):
    try:
        user = User.objects.get(username=username)

        template = loader.get_template('aureva_core/user_page.html')
        context = RequestContext(request, {'current_user': user})
        return HttpResponse(template.render(context))
    except User.DoesNotExist:
        return HttpResponse("No user with the name {0} was found.".format(username))


def track(request, username, title):

    # First we look to see if the user exists, then if the track title exists under the user's tracks.
    try:
        user = User.objects.get(username=username)

        try:
            track = Track.objects.get(title=title, user=user)
            template = loader.get_template('aureva_core/track.html')
            context = RequestContext(request, {'track': track, 'artist': user})
            return HttpResponse(template.render(context))

        # Track is not in user's tracks
        except Track.DoesNotExist:
            return HttpResponse("No track with the name {0} by {1} was found.".format(title, username))

    except User.DoesNotExist:
        return HttpResponse("No user with the name {0} was found.".format(username))


@login_required
def account_settings(request):
    template = loader.get_template('aureva_core/account_settings.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))