from django.conf.urls.defaults import patterns

urlpatterns = patterns('faq.views',
	(r'^(?P<program_id>\S+)/$', 'faq'),
)
