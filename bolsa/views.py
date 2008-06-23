from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from bolsa.models import ApplicationSession, ApplicantForm, ApplicantPastForm, ApplicantFutureForm, ApplicantSchoolForm, ApplicantCommitmentsForm
from django.newforms.util import ErrorDict
from django.utils.safestring import mark_safe
from django import newforms as forms


def get_form(form, data=None):
    if data:
        form = form(data, error_class=BolsaErrorDict)
    else:
        form = form()
    return form






class BolsaErrorDict(ErrorDict):
    def __init__(self, form):
        self.form = form
    def __unicode__(self):
        return self.as_ul()
    def as_ul(self):
        if not self: return u''
        return mark_safe(u'<ul class="errorlist">%s</ul>'
                % ''.join([u'<li>%s%s</li>' % (form[k].label, force_unicode(v))
                    for k, v in self.items()]))




def apply(request):
    if request.method == 'POST':
        session = ApplicationSession()
        session.save()
        return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/1/" % session.session_id)
    else:
        return render_to_response('bolsa/templates/apply.html')






def applicant(request, applicant_id):
    # guard for valid sessions and make sure user has authority to edit application
    session = ApplicationSession.objects.get(pk=applicant_id)
    if request.method == 'POST':
        q = request.POST.copy()
        # reconstruct dates
        birthdate = extract_date(q, 'birthdate')
        # create form and POSTed data to create an Applicant instance
        form = get_form(ApplicantForm, q)
        if form.is_valid():
            applicant = form.save(commit=False)
            # inject the session and save
            applicant.session = session
            applicant.save()
        
            # mark applicant step complete
            session.completed_step = 1
            session.save()
            # forward on to next step
            return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/2/" % session.session_id)
    else:
        # new application
        form = get_form(ApplicantForm)
        birthdate = None
    # form either came from failed submit or new form
    return render_to_response('bolsa/templates/1.html', {'applicant_id': applicant_id, 'form': form, 'birthdate': birthdate})


def extract_date(form, element):
    form[element] = "%s-%s-%s" % (form[element+'_year'], form[element+'_month'], form[element+'_day'])
    return {'day': form[element+'_day'], 'month': form[element+'_month'], 'year': form[element+'_year']}



def past(request, applicant_id):
    session = ApplicationSession.objects.get(pk=applicant_id)
    if request.method == 'POST':
        q = request.POST.copy()
        # reconstruct dates
        mission_start_date = extract_date(q, 'mission_start_date')
        mission_end_date = extract_date(q, 'mission_end_date')
        casp_date = extract_date(q, 'casp_date')
        sei_date = extract_date(q, 'sei_date')
        # create form and POSTed data to create an Applicant instance
        form = get_form(ApplicantPastForm, q)
        if form.is_valid():
            past = form.save(commit=False)
            # inject the session and save
            past.session = session
            past.save()
            
            # mark past step complete
            session.completed_step = 2
            session.save()
            # foward on to next step
            return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/3/" % session.session_id)
    else:
        form = get_form(ApplicantPastForm)
        mission_start_date = None
        mission_end_date = None
        casp_date = None
        sei_date = None
    
    # form either came from failed submit or new form
    return render_to_response('bolsa/templates/2.html', {'applicant_id': applicant_id, 'form': form, 'mission_start_date': mission_start_date, 'mission_end_date': mission_end_date, 'casp_date': casp_date, 'sei_date': sei_date})





def future(request, applicant_id):
    session = ApplicationSession.objects.get(pk=applicant_id)
    if request.method == 'POST':
        q = request.POST.copy()
        form = get_form(ApplicantFutureForm, q)
        if form.is_valid():
            future = form.save(commit=False)
            # inject the session and save
            future.session = session
            future.save()
            
            # mark future step complete
            session.completed_step = 3
            session.save()
            # forward on to next step
            return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/4/" % session.session_id)
    else:
        form = get_form(ApplicantFutureForm)
    
    # form either came from failed submit or new form
    return render_to_response('bolsa/templates/3.html', {'applicant_id': applicant_id, 'form': form})
    
    
    
    
def school(request, applicant_id):
    session = ApplicationSession.objects.get(pk=applicant_id)
    if request.method == 'POST':
        q = request.POST.copy()
        program_start_date = extract_date(q, 'program_start_date')
        form = get_form(ApplicantSchoolForm, q)
        if form.is_valid():
            school = form.save(commit=False)
            school.session = session
            school.save()
            session.completed_step = 4
            session.save()
            return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/5/" % session.session_id)
    else:
        form = get_form(ApplicantSchoolForm)
        program_start_date = None
    return render_to_response('bolsa/templates/4.html', { 'applicant_id': applicant_id, 'form': form, 'program_start_date': program_start_date })
    
def commitments(request, applicant_id):
    session = ApplicationSession.objects.get(pk=applicant_id)
    if request.method == 'POST':
        q = request.POST.copy()
        date = extract_date(q, 'date')
        form = get_form(ApplicantCommitmentsForm, q)
        if form.is_valid():
            commitments = form.save(commit=False)
            commitments.session = session
            commitments.save()
            session.completed_step = 5
            session.save()
            return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/confirm/" % session.session_id)
    else:
        form = get_form(ApplicantCommitmentsForm)
        date = None
    return render_to_response('bolsa/templates/5.html', {'applicant_id': applicant_id, 'form': form, 'date': date})

def confirm(request, applicant_id):
    session = ApplicationSession.objects.get(pk=applicant_id)
    if request.method == 'POST':
        q = request.POST.copy()
        confirm = q['confirm']
        if confirm == 'Y':
            return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/confirm/" % session.session_id)
    return render_to_response('bolsa/templates/6.html')

def done(request, applicant_id):
    session = ApplicationSession.objects.get(pk=applicant_id)
    session.completed_step = 6
    session.save()
    return HttpResponse("done")

