from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session
from Participation.forms import UserForm, ExperimenterForm, ParticipantsForm, ExperimentsForm, BidForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Participation.models import UserProfile
from Participation.models import Experiments, Experimenter, Participants, Bid
#from Participation.bing_search import run_query


def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def index(request):
    context = RequestContext(request)
    return render_to_response('Participation/index.html', context)

def registerExperimenter(request):
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
            'Participation/registerExperimenter.html',
            {'user_form': user_form, 'profile_form': experimenter_form, 'registered': registered},
            context)

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
        participant_form = ParticipantsForm()

    # Render the template depending on the context.
    return render_to_response(
            'Participation/registerParticipant.html',
            {'user_form': user_form, 'profile_form': participant_form, 'registered': registered},
            context)

def user_login(request):

    # Obtain our request's context.
    context = RequestContext(request)
    #cat_list = get_category_list()
    context_dict = {}
    #context_dict['cat_list'] = cat_list

    # If HTTP POST, pull out form data and process it.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Attempt to log the user in with the supplied credentials.
        # A User object is returned if correct - None if not.
        user = authenticate(username=username, password=password)

    # A valid user logged in?
        if user is not None:
            # Check if the account is active (can be used).
            # If so, log the user in and redirect them to the homepage.
            if user.is_active:

                u = User.objects.get(username__exact=username)
                experimenterP = Experimenter.objects.filter(user=u.id)
                if len(experimenterP)>0:
                    experimenterP = Experimenter.objects.get(user=u.id)
                    request.session['type_id'] = experimenterP.expter_id
                    request.session['type'] = "experimenter"
                    print(request.session['type'])
                    print(request.session['type_id'])
                else:
                    participantsP = Participants.objects.get(user=u.id)
                    request.session['type'] = "participants"
                    request.session['type_id'] = participantsP.part_id
                    print(request.session['type'])
                    print(request.session['type_id'])

                login(request, user)
                return HttpResponseRedirect('/Participation/')
            # The account is inactive; tell by adding variable to the template context.
            else:
                context_dict['disabled_account'] = True
                return render_to_response('Participation/login.html', context_dict, context)
        # Invalid login details supplied!
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('Participation/login.html', context_dict, context)

    # Not a HTTP POST - most likely a HTTP GET. In this case, we render the login form for the user.
    else:
        return render_to_response('Participation/login.html', context_dict, context)

def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/Participation/')


def about(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('Participation/about.html', context_dict, context)

def registerHome(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('Participation/registerHome.html', context_dict, context)

def add_experiments(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = ExperimentsForm(request.POST)
        expterId = request.session['type_id']
        print(expterId)
        # Have we been provided with a valid form?
        if form.is_valid():

            # Save the new category to the database.
            experiment = form.save(commit=False)
            experiment.expter_id_id=expterId
            form.save()

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = Experiments()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('Participation/add_experiments.html', {'form': form}, context)

def get_experiments_list(request):
    # Get the context from the request.
    context = RequestContext(request)
    type_id = request.session['type_id']
    type = request.session["type"]

    context_dict = {}
    if request.method == 'POST':

        experimentId=request.POST['el_id_id']
        form = BidForm(request.POST)

        if form.is_valid():

            experimentList = form.save(commit=False)
            experimentList.el_id_id = experimentId
            experimentList.part_id_id = type_id
            experimentList.save()

        else:
            print form.errors

    else:

        if type == "experimenter":
            exp_list = Experiments.objects.filter(expter_id_id=type_id)
        else:
            exp_list = Experiments.objects.all()
            bid_list = Bid.objects.filter(part_id_id=type_id)

            for b in bid_list:
                exp_list = exp_list.exclude(el_id=b.el_id.el_id)
        context_dict['exp_list'] = exp_list

    return render_to_response('Participation/experiments_list.html', context_dict , context)

def profile(request):
    context = RequestContext(request)
    context_dict = {}
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('Participation/profile.html', context_dict, context)

def sendmail(request, elid_url):
    context = RequestContext(request)
    if request.method == 'POST':
        from django.core.mail import EmailMultiAlternatives
        artists = request.POST.getlist('email[]')

        for email in artists:
            from_email = 'participantswanted2014@gmail.com'
            text_content = 'congratulations'
            html_content = ('<p>Dear Participant,</p>'
                        '<p>Thank you for expressing your interest in one of our Experiment. We are glad to inform you that your bid is successfully. The Experimenter will contact you within the next 24 hours. Thank you and have a nice day.</p>'
                        '<p>Best Wishes,<br>'
                        'ParticipantsWanted'
                        '</p>')
            email = EmailMultiAlternatives('ParticipantsWanted2014 - Successful Bid Application', text_content, from_email , to=[email])
            email.attach_alternative(html_content, "text/html")
            email.send()
    return HttpResponseRedirect('/Participation/experiments_list/'+elid_url+'/')

def get_pastexperiments_list(request):

    # Get the context from the request.
    context = RequestContext(request)
    type_id = request.session['type_id']

    context_dict = {}

    exp_list = Bid.objects.filter(part_id_id=type_id)

    context_dict['exp_list'] = exp_list

    return render_to_response('Participation/pastexperiments_list.html', context_dict , context)

def getUser(request, elid_url):
    exp_id = decode_url(elid_url)
    context = RequestContext(request)
    context_dict = {}

    part_list = Bid.objects.filter(el_id_id = exp_id)

    userid_list = list()
    for a in part_list:
        userid = a.part_id.part_id
        userid_list.append(userid)

    user_userid_list = list()
    for user in userid_list:
        user_userid_list.append(Participants.objects.filter(part_id = user))

    user_email_list = list()
    for b in user_userid_list:
        user_user_id = b.values('user_id')
        user_email_list.append(User.objects.filter(id = user_user_id))

    context_dict['user_email_list'] = user_email_list

    return render_to_response('Participation/notify.html', context_dict , context)