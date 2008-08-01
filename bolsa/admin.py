from django.contrib import admin
from incentivo.bolsa.models import ApplicationSession, RequestLog, Applicant, ApplicantPast, ApplicantFuture, ApplicantSchool, ApplicantCommitments

############ Admin form declarations #################
admin.site.register(ApplicationSession)
admin.site.register(RequestLog)
admin.site.register(Applicant)
admin.site.register(ApplicantPast)
admin.site.register(ApplicantFuture)
admin.site.register(ApplicantSchool)
admin.site.register(ApplicantCommitments)

