from django.contrib import admin
from faq.models import FAQ, Program


############ Admin form declarations #################
admin.site.register(Program)
admin.site.register(FAQ)
