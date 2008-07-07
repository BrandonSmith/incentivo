from django.conf.urls.defaults import patterns

urlpatterns = patterns('bolsa.views',
	(r'^apply/$', 'apply'),
	(r'^apply/(?P<applicant_id>\S+)/1/$', 'applicant'),
	(r'^apply/(?P<applicant_id>\S+)/2/$', 'past'),
	(r'^apply/(?P<applicant_id>\S+)/3/$', 'future'),
	(r'^apply/(?P<applicant_id>\S+)/4/$', 'school'),
	(r'^apply/(?P<applicant_id>\S+)/5/$', 'commitments'),
	(r'^apply/(?P<applicant_id>\S+)/6/$', 'confirm'),
	(r'^apply/(?P<applicant_id>\S+)/done/$', 'done'),
)
