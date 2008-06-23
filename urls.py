from django.conf.urls.defaults import *
from django.contrib.auth.models import *
from django.contrib import databrowse
from django import newforms as forms
from incentivo.bolsa.models import Applicant, ApplicantForm
from django.conf import settings

urlpatterns = patterns('',
	(r'^admin/', include('django.contrib.admin.urls')),
	(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.OTHER_MEDIA_ROOT}),
	(r'^bolsa-de-estudo/', include('incentivo.bolsa.urls')),
	(r'^databrowse/(.*)', databrowse.site.root),
	(r'^contact/', include('contact_form.urls')),
)

databrowse.site.register(User)

#(r'^bolsa/success/$', 'incentivo.bolsa.views.success'),
