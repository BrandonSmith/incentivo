# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.newforms import ModelForm
from django import newforms as forms
from incentivo.utils import UUIDField
import bolsa
from django.core.validators import AlwaysMatchesOtherField

class ApplicationSession(models.Model):

    session_id = UUIDField(primary_key=True)
    completed_step = models.IntegerField(default=0)
    
    def __unicode__(self):
        return "%s: %s" % (self.session_id, self.completed_step)
    
    class Admin:
        pass


class Applicant(models.Model):
    """An Applicant describes basic information about someone filling out an application"""

    session = models.OneToOneField(ApplicationSession, editable=False)
    
    last_name = models.CharField("Sobrenome", max_length=50, help_text="Favor preencher o campo 'Sobrenome'")
    first_name = models.CharField("Nome", max_length=50, help_text="Favor preencher o campo 'Nome'")
    middle_name = models.CharField("Nome do meio", blank=True, max_length=50)
    
    gender = models.CharField("Sexo", max_length=1, blank=True, choices=bolsa.GENDER_CHOICES)
    birthdate = models.DateField("Data de nascimento", help_text="Favor preencher o campo 'Data de nascimento'")
    married = models.BooleanField("Estado civil", blank=True)
    head_of_household = models.BooleanField("Chefe de Família?", blank=True)
    number_of_children = models.IntegerField("Número de filhos", blank=True)
    
    address = models.CharField("Endereço", blank=True, max_length=150)
    address2 = models.CharField("Endereço 2", blank=True, max_length=150)
    city = models.CharField("Cidade", max_length=100)
    state = models.CharField("Província", max_length=2)
    zip_code = models.CharField("Código postal", blank=True, max_length=10)
    country = models.CharField("País", blank=True, max_length=25, choices=bolsa.COUNTRY_CHOICES)
    
    email = models.EmailField("E-mail (por favor utilizar um endereço de E-mail que você acessa com freqüência. Todo contato da Incentivo será via comunicação eletrônica)", max_length=50, help_text="Favor preencher o campo 'E-mail'")
    business_telephone = models.CharField("Telefone commercial", max_length=15)
    home_telephone = models.CharField("Telefone residencial", max_length=15)
    
    emergency_name = models.CharField("Nome de parente mais próximo que não mora com você ou outra pessoa que saberá do seu paradeiro", max_length=100, help_text="Favor informar o nome de alguém que saberá do seu paradeiro")
    emergency_email = models.EmailField("Email", blank=True, max_length=50)
    emergency_phone = models.CharField("Telefone", help_text="Favor informar o número de telefone da pessoa que saberá do seu paradeiro", max_length=15)

    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)
    
    class Admin:
        pass

class ApplicantForm(ModelForm):
    email2 = forms.EmailField(label="Confirmar E-mail")
    
    def clean_email2(self):
        email2_value = self.data['email2']
        email_value = self.data['email']
        if not email2_value == email_value:
            raise forms.ValidationError('Confirming email must match')
    
    class Meta:
        model = Applicant








class ApplicantPast(models.Model):
    """An ApplicantPast is information about the individuals past education"""

    session = models.OneToOneField(ApplicationSession, editable=False)
    
    casp_date = models.DateField("Datas em que foram realizados os cursos", help_text="Favor informar a data que você concluiu o curso CASP")
    casp_instructor_name = models.CharField("Nome do Instrutor", max_length=100, help_text="Favor informar o nome do instrutor do curso CASP")
    casp_instructor_phone = models.CharField("Telefone", max_length=15, blank=True, help_text="Favor informar o nome do instrutor do curso CASP")
    
    sei_date = models.DateField("Datas em que foram realizados os cursos", help_text="Favor informar a data que você concluiu o curso Planejar Para o Sucesso")
    sei_instructor_name = models.CharField("Nome do Instrutor", max_length=100, help_text="Favor informar o nome do instrutor do curso Planejar Para o Sucesso")
    sei_instructor_phone = models.CharField("Telefone", blank=True, max_length=15)
    
    employer = models.CharField("Meu trabalho atual", max_length=100, blank=True, help_text="Favor informar o seu trabalho atual")
    salary = models.IntegerField("Remuneração mensal (não ponha centavos)", blank=True, help_text="Favor informar a sua remuneração mensal")
    
    spouse_employed = models.BooleanField("O seu cônjuge trabalha ou tem alguma renda mensal? (Caso sim, por favor indique em que trabalha no campo abaixo)")
    spouse_employer = models.CharField(max_length=100, blank=True, help_text="Favor informar o trabalho atual do seu cônjuge")
    spouse_salary = models.IntegerField("Remuneração mensal do seu cônjuge (não ponha centavos)", blank=True, help_text="Favor informar o valor da remuneração mensal do seu cônjuge")
    
    class Admin:
        pass

class ApplicantPastForm(ModelForm):
    class Meta:
        model = ApplicantPast






class ApplicantFuture(models.Model):

    session = models.OneToOneField(ApplicationSession, editable=False)
    
    future_employer = models.CharField("Que trabalho deseja conseguir depois da conclusão do curso?", max_length=100, help_text="Favor informar que trabalho deseja conseguir depois da conclusão do curso")
    future_salary = models.IntegerField("Renda mensal aproximada (não ponha centavos)", help_text="Favor informar a renda mensal aproximada deste trabalho")
    reason = models.TextField("Por que você quer seguir esta profissão?", help_text="Favor informar por que você quer seguir esta profissão")

    essay_plan = models.TextField("Seu Plano - No campo abaixo por favor explique detalhadamente o seu plano; O que já fez, está fazendo e vai fazer para conseguir os fundos necessários para completar este curso? Como este curso se encaixa no seu plano do longo prazo? Quais são os passos que você já tomou, está tomando e vai tomar para conseguir trabalho após o curso? (Máximo de 2.500 caracteres)", help_text="Favor responder a Redação 1 – Seu Plano")
    essay_reason = models.TextField("No campo abaixo por favor explique por que você deve receber o auxílio da Incentivo para ajudar com o seu curso. (Máximo de 2.500 caracteres)", help_text="Favor responder a Redação 2 – Por Que Eu Devo Receber uma Bolsa")
    essay_next = models.TextField("No campo abaixo por favor explique o que você entende ser “passar adiante” e como você passará adiante caso seja aprovado para receber uma bolsa. (Máximo de 2.500 caracteres)", help_text="Favor responder a Redação 3 – Passar Adiante")
    
    class Admin:
        pass

class ApplicantFutureForm(ModelForm):
    class Meta:
        model = ApplicantFuture




class ApplicantSchool(models.Model):

    session = models.OneToOneField(ApplicationSession, editable=False)

    school_name = models.CharField("Nome do estabelecimento de ensino", max_length=50, help_text="Favor informa o nome do estabelecimento de ensino")
    program_name = models.CharField("Curso de estudo ou especialização", max_length=50, help_text="Favor informar o tipo de curso ou especialização")
    program_duration = models.IntegerField("Duração do programa (nº de meses)", help_text="Favor informar a duração do curso em meses")
    program_start_date = models.DateField(help_text="Favor informar a data que pretende começar o curso")
    program_cost = models.IntegerField("Valor da mensalidade do curso (não ponha centavos)", help_text="Favor informar o valor da mensalidade do curso")
    program_city = models.CharField("Cidade do estabelecimento", max_length=50, help_text="Favor informar a cidade na qual o curso é oferecido")
    pay_half = models.BooleanField("Pode pagar 50% do seu curso?")
    program_url = models.URLField("Site de internet do estabelecimento/curso", blank=True)
    
    class Admin:
        pass

class ApplicantSchoolForm(ModelForm):
    class Meta:
        model = ApplicantSchool




class ApplicantCommitments(models.Model):

    session = models.OneToOneField(ApplicationSession, editable=False)

    commitment_moving_foward = models.BooleanField("Me comprometo a cumprir a filosofia Passar Adiante", help_text="Por favor lea e marque cada compromisso para poder prosseguir. Caso não esteja disposto a aceitar o compromisso, feche a janela do seu browser")
    commitment_own_money = models.BooleanField()
    commitment_good_student = models.BooleanField()
    commitment_faith = models.BooleanField()
    
    signature = models.CharField(max_length=150)
    date = models.DateField()
    
    ward = models.CharField(max_length=100)
    bishop_name = models.CharField(max_length=100)
    bishop_phone = models.PhoneNumberField()
    
    additional_comments = models.TextField()
    
    pledge = models.BooleanField()
    
    class Admin:
        pass





