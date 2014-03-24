from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from Participation.forms import UserForm, ExperimenterForm, ParticipantsForm
from django.contrib.auth import authenticate, login, logout

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def index(request):
    context = RequestContext(request)
    return render_to_response('Participation/index.html', context)

def registerExperiment(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        experimenter_form = ExperimenterForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and experimenter_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = experimenter_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, experimenter_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        experimenter_form = ExperimenterForm()

    # Render the template depending on the context.
    return render_to_response(
        './Participation/registerExperimenter.html',
            {'user_form': user_form, 'profile_form': experimenter_form, 'registered': registered},
            context)

def register(request):
    return render_to_response('/registerExperimenter.html')

def registerParticipant(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        participant_form = ParticipantsForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and participant_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = participant_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, participant_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = ParticipantsForm()

    # Render the template depending on the context.
    return render_to_response(
            './registerExperimenter.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

# def user_login(request):
#     # Obtain our request's context.
#     context = RequestContext(request)
#     cat_list = get_category_list()
#     context_dict = {}
#     context_dict['cat_list'] = cat_list
#
#     # If HTTP POST, pull out form data and process it.
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         # Attempt to log the user in with the supplied credentials.
#         # A User object is returned if correct - None if not.
#         user = authenticate(username=username, password=password)
#
#         # A valid user logged in?
#         if user is not None:
#             # Check if the account is active (can be used).
#             # If so, log the user in and redirect them to the homepage.
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/Participation/')
#             # The account is inactive; tell by adding variable to the template context.
#             else:
#                 context_dict['disabled_account'] = True
#                 return render_to_response('Participation/login.html', context_dict, context)
#         # Invalid login details supplied!
#         else:
#             print "Invalid login details: {0}, {1}".format(username, password)
#             context_dict['bad_details'] = True
#             return render_to_response('Participation/login.html', context_dict, context)
#
#     # Not a HTTP POST - most likely a HTTP GET. In this case, we render the login form for the user.
#     else:
#         return render_to_response('Participation/login.html', context_dict, context)
