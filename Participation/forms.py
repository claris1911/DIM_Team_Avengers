from django.contrib.auth.models import User
from django import forms
from Participation.models import Experiments, Experimenter, Participants, Bid, UserProfile

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a Username.")
    first_name = forms.CharField(help_text="Please enter your First Name.")
    last_name = forms.CharField(help_text="Please enter your Last Name.")
    email = forms.CharField(help_text="Please enter your Email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'is_staff')

class ExperimenterForm(forms.ModelForm):

    website = forms.URLField(help_text="Please enter your website.", required=False)
    #picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
    title = forms.CharField(help_text="Please enter your Title.")
    school = forms.CharField(help_text="Please enter your School.")
    website = forms.URLField(help_text="Please enter your website.", required=False)
    contact_no = forms.CharField(help_text="Please enter your Contact No.")

    class Meta:
        model = Experimenter
        fields = ('title', 'school', 'website', 'contact_no')
    #'picture',

class ParticipantsForm(forms.ModelForm):

  #  picture = forms.ImageField(help_text="Select a Profile Image to upload.", required=False)
    age = forms.IntegerField(help_text="Please enter your Age.")
    sex = forms.CharField(help_text="Please enter your Gender.")
    language = forms.CharField(help_text="Please enter your Language.")
    country = forms.CharField(help_text="Please enter your Country.")
    education = forms.CharField(help_text="Please enter your Education Level.")
    rating = forms.CharField(help_text="Please enter your Rating.")


    class Meta:
        model = Participants
        fields = ('age', 'sex', 'language', 'country', 'education', 'rating')

class ExperimentsForm(forms.ModelForm):

    name = forms.CharField(max_length=128, help_text="Please enter the Experiment name.")
    startDate = forms.DateField(help_text="Please enter the Start Date (MM-DD-YYYY).")
    endDate = forms.DateField(help_text="Please enter the End Date (MM-DD-YYYY).")
    reward = forms.IntegerField(help_text="Please enter the Reward.")
    noOfParticipant = forms.IntegerField(help_text="Please enter the No. of Participants.")

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Experiments
        fields = ('name', 'startDate', 'endDate', 'reward', 'noOfParticipant')

class BidForm(forms.ModelForm):

    el_id_id = forms.IntegerField()
    part_id_id = forms.IntegerField()

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Bid
        fields = ('el_id_id', 'part_id_id')

class UserProfileForm(forms.ModelForm):

    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')