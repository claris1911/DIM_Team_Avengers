from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	# A required line - links a UserProfile to User.
	user = models.OneToOneField(User)

	# The additional attributes we wish to include.
	website = models.URLField(blank=True)
	#picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.user.username


class Experimenter(models.Model):
    # A required line - links a UserProfile to User.
    user = models.OneToOneField(User)
    #picture = models.ImageField(upload_to='profile_images', blank=True)
    expter_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16)
    school = models.CharField(max_length=48)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    contact_no = models.IntegerField()

class Participants(models.Model):
    user = models.OneToOneField(User)
    part_id = models.AutoField(primary_key=True)
    age = models.IntegerField()
    sex = models.CharField(max_length=12)
    language = models.CharField(max_length=48)
    country = models.CharField(max_length=128)
    education = models.CharField(max_length=128)
    rating = models.CharField(max_length=12)


class Experiments(models.Model):
    el_id = models.AutoField(primary_key=True)
    expter_id = models.ForeignKey(Experimenter)
    name = models.CharField(max_length=128)
    startDate = models.DateField(auto_now_add=True)
    endDate = models.DateField()
    reward = models.CharField(max_length=128)
    noOfParticipant = models.IntegerField()

class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    el_id = models.ForeignKey(Experiments)
    part_id = models.ForeignKey(Participants)