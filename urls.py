from django.conf.urls.defaults import *
from django.contrib.auth.models import *
from django.contrib import databrowse
from django import forms
from incentivo.bolsa.models import Applicant, ApplicantForm, ApplicantPast
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/(.*)', admin.site.root),
	(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.OTHER_MEDIA_ROOT}),
	(r'^bolsa-de-estudo/', include('incentivo.bolsa.urls')),
	(r'^faq/', include('incentivo.faq.urls')),
	#(r'^databrowse/(.*)', databrowse.site.root),
	#(r'^contact/', include('contact_form.urls')),
)

#databrowse.site.register(Applicant)
#databrowse.site.register(ApplicantPast)

#(r'^bolsa/success/$', 'incentivo.bolsa.views.success'),
