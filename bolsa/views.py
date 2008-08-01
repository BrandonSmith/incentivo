from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from bolsa.models import ApplicationSession, Applicant, ApplicantForm, ApplicantPastForm, ApplicantFutureForm, ApplicantSchoolForm, ApplicantCommitmentsForm, RequestLog, ApplicantPast, ApplicantCommitments, ApplicantFuture, ApplicantSchool
from django.forms.util import ErrorDict
from django.utils.safestring import mark_safe
from django import forms
from django.conf import settings


# ------------------- UTILITY METHODS -----------------------------------------#
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


def get_form(form, data=None, instance=None):
    #if instance:
    #    form = form(data, instance=instance, error_class=BolsaErrorDict)
    #else data:
    #    form = form(data, error_class=BolsaErrorDict)
    return form(data, instance=instance, error_class=BolsaErrorDict)


def log_request(session, request, step):
    log = RequestLog(session=session, log=repr(request), step=step)
    log.save()


def extract_date(data, element):
    data[element] = "%s-%s-%s" % (data[element+'_year'], data[element+'_month'], data[element+'_day'])
    return {'day': data[element+'_day'], 'month': data[element+'_month'], 'year': data[element+'_year']}


def swindle_date(data):
    return {'day': data.day, 'month': data.month, 'year': data.year}



# ---------------------- VIEW METHODS -----------------------------------------#

def apply(request):
    if request.method == 'POST':
        data = request.POST.copy()
        if 'applicant_id' in data:
            try:
                session = ApplicationSession.objects.get(pk=data['applicant_id'])
                applicant = Applicant.objects.get(session=session)
            except (ApplicationSession.DoesNotExist, Applicant.DoesNotExist):
                return render_to_response('bolsa/templates/apply.html', {'applicant_id': data['applicant_id']})
            return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, session.completed_step + 1))
        else:
            session = ApplicationSession()
            session.save()
            return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/1/" % session.session_id)
    else:
        return render_to_response('bolsa/templates/apply.html')






def applicant(request, applicant_id):

    step = 1    
    session = ApplicationSession.objects.get(pk=applicant_id)
    
    if request.method == 'POST':
    
        data = request.POST.copy()
        log_request(session, data, 1)
        # reconstruct dates
        birthdate = extract_date(data, 'birthdate')
        try:
            instance = Applicant.objects.get(session=session)
            form = get_form(ApplicantForm, data, instance)
            if form.is_valid():
                instance.delete()
                form.save()
                return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, step+1))
        except Applicant.DoesNotExist:
            form = get_form(ApplicantForm, data)
            if form.is_valid():
                applicant = form.save(commit=False)
                # inject the session and save
                applicant.session = session
                applicant.save()
                # mark applicant step complete
                session.completed_step = 1
                session.save()
                # send inital email with application password
                if not settings.DEBUG:
                    from django.core.mail import send_mail
                    send_mail('Incentivo Bolsa Form Password: %s' % session.session_id, session.session_id, 'bolsa@incentivo.org.br', [applicant.email], fail_silently=False)
                return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, step+1))
    
    else:
        try:
            instance = Applicant.objects.get(session=session)
            form = get_form(ApplicantForm, instance=instance)
            birthdate = swindle_date(instance.birthdate)
        except Applicant.DoesNotExist:
            form = get_form(ApplicantForm)
            birthdate = None
    
    # form either came from failed submit or new form
    return render_to_response('bolsa/templates/1.html', {'applicant_id': applicant_id, 'form': form, 'birthdate': birthdate})








def past(request, applicant_id):

    step = 2
    session = ApplicationSession.objects.get(pk=applicant_id)
    
    # guard against skipping to a later section
    # allow for navigating back to previously entered
    if step > session.completed_step+1:
        return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, session.completed_step+1))
    
    if request.method == 'POST':
    
        data = request.POST.copy()
        log_request(session, data, step)
        # reconstruct dates
        mission_start_date = extract_date(data, 'mission_start_date')
        mission_end_date = extract_date(data, 'mission_end_date')
        casp_date = extract_date(data, 'casp_date')
        sei_date = extract_date(data, 'sei_date')
        
        try:
            instance = ApplicantPast.objects.get(session=session)
            form = get_form(ApplicantPastForm, data, instance)
            if form.is_valid():
                instance.delete()
                form.save()
                return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, step+1))
        except ApplicantPast.DoesNotExist:
            form = get_form(ApplicantPastForm, data)
            if form.is_valid():
                past = form.save(commit=False)
                past.session = session
                past.save()                
                session.completed_step = step
                session.save()
                return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, step+1))
    
    else:
        try:
            instance = ApplicantPast.objects.get(session=session)
            form = get_form(ApplicantPastForm, instance=instance)
            mission_start_date = swindle_date(instance.mission_start_date)
            mission_end_date = swindle_date(instance.mission_end_date)
            casp_date = swindle_date(instance.casp_date)
            sei_date = swindle_date(instance.sei_date)
        except ApplicantPast.DoesNotExist:
            form = get_form(ApplicantPastForm)
            mission_start_date = None
            mission_end_date = None
            casp_date = None
            sei_date = None
    
    # form either came from failed submit or new form
    return render_to_response('bolsa/templates/2.html', {'applicant_id': applicant_id, 'form': form, 'mission_start_date': mission_start_date, 'mission_end_date': mission_end_date, 'casp_date': casp_date, 'sei_date': sei_date})





def future(request, applicant_id):

    step = 3
    
    session = ApplicationSession.objects.get(pk=applicant_id)
    
    # guard against skipping to a later section
    # allow for navigating back to previously entered
    if step > session.completed_step+1:
        return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, session.completed_step+1))
    
    if request.method == 'POST':
        
        data = request.POST.copy()
        log_request(session, data, step)
        
        try:
            instance = ApplicantFuture.objects.get(session=session)
            form = get_form(ApplicantFutureForm, data, instance)
            if form.is_valid():
                instance.delete()
                form.save()
                return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, step+1))
        except ApplicantFuture.DoesNotExist:
            form = get_form(ApplicantFutureForm, data)
            if form.is_valid():
                future = form.save(commit=False)
                future.session = session
                future.save()
                session.completed_step = step
                session.save()
                return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, step+1))
    else:
        try:
            instance = ApplicantFuture.objects.get(session=session)
            form = get_form(ApplicantFutureForm, instance=instance)
        except ApplicantFuture.DoesNotExist:
            form = get_form(ApplicantFutureForm)
    return render_to_response('bolsa/templates/3.html', {'applicant_id': applicant_id, 'form': form})

    
    
    
    
def school(request, applicant_id):

    step = 4
    
    session = ApplicationSession.objects.get(pk=applicant_id)
    
    # guard against skipping to a later section
    # allow for navigating back to previously entered
    if step > session.completed_step+1:
        return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, session.completed_step+1))
    
    if request.method == 'POST':
        
        data = request.POST.copy()
        log_request(session, data, step)
        # recreate the dates
        program_start_date = extract_date(data, 'program_start_date')
        
        try:
            instance = ApplicantSchool.objects.get(session=session)
            form = get_form(ApplicantSchoolForm, data)
            if form.is_valid():
                instance.delete()
                form.save()
                return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, step+1))
        except ApplicantSchool.DoesNotExist:
            form = get_form(ApplicantSchoolForm, data)
            if form.is_valid():
                school = form.save(commit=False)
                school.session = session
                school.save()
                session.completed_step = step
                session.save()
                return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, step+1))
    else:
        try:
            instance = ApplicantSchool.objects.get(session=session)
            form = get_form(ApplicantSchoolForm, instance=instance)
            program_start_date = swindle_date(instance.program_start_date)
        except ApplicantSchool.DoesNotExist:
            form = get_form(ApplicantSchoolForm)
            program_start_date = None

    return render_to_response('bolsa/templates/4.html', {'applicant_id': applicant_id, 'form': form, 'program_start_date': program_start_date})
        






def commitments(request, applicant_id):
    
    step = 5
    session = ApplicationSession.objects.get(pk=applicant_id)
    
    # guard against skipping to a later section
    # allow for navigating back to previously entered
    if step > session.completed_step+1:
        return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, session.completed_step+1))
    
    if request.method == 'POST':
    
        data = request.POST.copy()
        log_request(session, data, step)
        # recreate the dates
        date = extract_date(data, 'date')
        
        try:
            instance = ApplicantCommitments.objects.get(session=session)
            form = get_form(ApplicantCommitmentsForm, data, instance)
            if form.is_valid():
                instance.delete()
                form.save()
                return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, step+1))
        except ApplicantCommitments.DoesNotExist:
            form = get_form(ApplicantCommitmentsForm, data)
            if form.is_valid():
                commitments = form.save(commit=False)
                commitments.session = session
                commitments.save()
                session.completed_step = step
                session.save()
                return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, step+1))
    else:
        try:
            instance = ApplicantCommitments.objects.get(session=session)
            form = get_form(ApplicantCommitmentsForm, instance=instance)
            date = swindle_date(instance.date)
        except ApplicantCommitments.DoesNotExist:
            form = get_form(ApplicantCommitmentsForm)
            date = None
    return render_to_response('bolsa/templates/5.html', {'applicant_id': applicant_id, 'form': form, 'date': date})





def confirm(request, applicant_id):
    
    step = 6
    
    session = ApplicationSession.objects.get(pk=applicant_id)
    
    # guard against skipping to a later section
    # allow for navigating back to previously entered
    if step > session.completed_step+1:
        return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, session.completed_step+1))
    
    if request.method == 'POST':
        data = request.POST.copy()
        confirm = data['confirm']
        if confirm == 'Y':
            session.completed_step = step
            session.save()
            return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/done/" % session.session_id)
    return render_to_response('bolsa/templates/6.html')






def done(request, applicant_id):
    
    step = 7
    
    session = ApplicationSession.objects.get(pk=applicant_id)
    
    if step > session.completed_step+1:
        return HttpResponseRedirect("/bolsa-de-estudo/apply/%s/%s/" % (session.session_id, session.completed_step+1))
    
    applicant = Applicant.objects.get(session=session)
    
    # send final email with next steps
    if not settings.DEBUG:
        from django.core.mail import send_mail
        send_mail('Incentivo Bolsa Form Complete: %s' % session.session_id, session.session_id, 'bolsa@incentivo.org.br', [applicant.email], fail_silently=False)
            
    session.completed_step = step
    session.save()
    
    return HttpResponse("done")

