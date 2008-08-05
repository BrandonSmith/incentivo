from django.shortcuts import render_to_response
from faq.models import FAQ

def faq(request, program_id):
    faqs = FAQ.objects.filter(program=program_id)
    return render_to_response('faq/templates/faq_display.html', {'faqs': faqs})


