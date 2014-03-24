from django.conf.urls import patterns, url
from Participation import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^registerHome/$', views.registerHome, name='registerHome'),
    url(r'^registerParticipant/$', views.registerParticipant, name='registerParticipant'),
    url(r'^registerExperimenter/$', views.registerExperimenter, name='registerExperimenter'),
    #url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^add_experiments/$', views.add_experiments, name='add_experiments'), # NEW MAPPING!
    url(r'^experiments_list/(?P<elid_url>\w+)/email/$', views.sendmail, name='email'),
    url(r'^experiments_list/$', views.get_experiments_list, name='experiments_list'),
    url(r'^pastexperiments_list/$', views.get_pastexperiments_list, name='pastexperiments_list'),
    url(r'^experiments_list/(?P<elid_url>\w+)/$', views.getUser, name='getuser')
)