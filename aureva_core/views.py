# Most fundamental imports
from django.template import RequestContext, loader
from django.shortcuts import render

# Helpers, assistant functions
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

# Authentication
from aureva_core.forms import UserForm, UserProfileForm, TrackForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Custom models to be used
from aureva_core.models import Track, Review, ReviewRating


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

    # Check if this is a POST request
    if request.method == 'POST':

        # Check if input is empty or not
        if request.POST.get('username') and request.POST.get('password'):

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

@login_required
def submit_review(request):
    if request.method == 'POST':

        # Check if we have the necessary data
        if request.POST.get('review-text') and request.POST.get('track'):
            text = request.POST['review-text']
            track = Track.objects.get(id=request.POST['track'])
            user = request.user

            # Only one review per track per person. If changes are submitted, change the text and set rating to zero.
            prior_review = Review.objects.filter(user=user, track=track)
            if len(prior_review) > 0:
                prior_review = prior_review[0]
                prior_review.text = text
                prior_review.reviewrating_set.all().delete()
                prior_review.save()
            else:
                review = Review(track=track, user=user, text=text)
                review.save()

            return HttpResponse(0)

        else:
            return HttpResponse(1)

    else:  # No GETs allowed
        raise SuspiciousOperation()

def review_vote(request):
    if request.method == 'POST':

        # Make sure we have the right data
        if request.POST.get('vote') and request.POST.get('review_id'):

            # User must be logged in
            if request.user.is_authenticated():
                user = request.user
                review = Review.objects.get(id=request.POST['review_id'])
                vote = True if request.POST['vote'] == 'true' else False  # Gets passed as string, unfortunately
                prev_rating = ReviewRating.objects.filter(user=user, review=review)

                # We don't want a set, we want the first one, but we can't access it if it doesn't exist.
                if prev_rating:
                    prev_rating = prev_rating[0]

                # If user has already voted on this, change rating if different and delete if same button
                if prev_rating:
                    if prev_rating.vote != vote:
                        prev_rating.vote = vote
                        prev_rating.save()
                        return HttpResponse(0)
                    else:
                        prev_rating.delete()
                        return HttpResponse(0)
                else:
                    rating = ReviewRating(user=user, review=review, vote=vote)
                    rating.save()
                    return HttpResponse(0)
            else:
                return HttpResponseBadRequest
        else:
            messages.error(request, 'You must be logged in to rate reviews.')
            return HttpResponse(1)
    else:
        raise SuspiciousOperation()

def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        links = (json.loads(user.userprofile.links) if user.userprofile.links else [])
        template = loader.get_template('aureva_core/user_page.html')
        context = RequestContext(request, {'current_user': user, 'current_user_links': links})
        return HttpResponse(template.render(context))
    except User.DoesNotExist:
        return HttpResponse("No user with the name {0} was found.".format(username))


def track(request, username, slug):

    # First we look to see if the user exists, then if the track title exists under the user's tracks.
    try:
        user = User.objects.get(username=username)

        try:
            track = Track.objects.get(slug=slug, user=user)
            tags = (json.loads(track.tags) if track.tags else [])
            reviews = track.review_set.all()
            template = loader.get_template('aureva_core/track.html')

            made_reviews = voted_reviews = {}
            # Get if browser user made or voted on any of these reviews
            if request.user.is_authenticated():
                made_reviews = [review.id for review in reviews if review.user == request.user]
                voted = [review for review in reviews if review in [rating.review for rating in review.reviewrating_set.filter(user=request.user)]]
                for review in voted:
                    voted_reviews[review.id] = review.reviewrating_set.get(user=request.user).vote

            context = RequestContext(request, {'track': track, 'artist': user, 'tags': tags, 'reviews': reviews,
                                               'made_reviews': made_reviews, 'voted_reviews': voted_reviews})

            return HttpResponse(template.render(context))

        # Track is not in user's tracks
        except Track.DoesNotExist:
            return HttpResponse('No track with the name "{0}" by {1} was found.'.format(slug, username))

    except User.DoesNotExist:
        return HttpResponse('No user with the name "{0}" was found.'.format(username))


@login_required
def account_settings(request):
    template = loader.get_template('aureva_core/account_settings.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def sandbox(request):
    template = loader.get_template('aureva_core/sandbox.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


@login_required
def create(request):

    # Avoid too much repeating code here with the use of a 'retval' response holder variable
    retval = None

    if request.method == 'POST':
        track_form = TrackForm(request.POST, request.FILES)

        if track_form.is_valid():
            # Save everything else without commit first, then link to current user
            to_commit = track_form.save(commit=False)
            to_commit.user = request.user

            to_commit.save()

            # Redirect to finished track page upon successful submission of form and upload of track
            track_url = '/aureva/user/' + to_commit.user.username + '/' + to_commit.slug
            retval = HttpResponseRedirect(track_url)

        else:  # If there are errors in the form, print them and then display them to the user
            print(track_form.errors)
            messages.error(request, 'There were errors in submitting this form. Please check your input and try again.')

    else:
        track_form = TrackForm()

    if not retval:  # Default, when first rendering the page or if errors persist
        template = loader.get_template('aureva_core/create.html')
        context = RequestContext(request, {'track_form': track_form})
        retval = HttpResponse(template.render(context))

    return retval