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
    city = models.CharField("Cidade", max_length=100, help_text="Favor informar o nome de sua cidade")
    state = models.CharField("Província", max_length=2, help_text="Favor informar o nome de seu estado")
    zip_code = models.CharField("Código postal", blank=True, max_length=10)
    country = models.CharField("País", blank=True, max_length=25, choices=bolsa.COUNTRY_CHOICES)
    
    email = models.EmailField("E-mail (por favor utilizar um endereço de E-mail que você acessa com freqüência. Todo contato da Incentivo será via comunicação eletrônica)", max_length=50, help_text="Favor preencher o campo 'E-mail'")
    business_telephone = models.CharField("Telefone commercial", blank=True, max_length=15)
    home_telephone = models.CharField("Telefone residencial", max_length=15, help_text="Favor informar o número de seu telefone residencia")
    
    
    
    emergency_name = models.CharField("Nome de parente mais próximo que não mora com você ou outra pessoa que saberá do seu paradeiro", max_length=100, help_text="Favor informar o nome de alguém que saberá do seu paradeiro")
    emergency_email = models.EmailField("Email", blank=True, max_length=50)
    emergency_phone = models.CharField("Telefone", help_text="Favor informar o número de telefone da pessoa que saberá do seu paradeiro", max_length=15)

    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)
    
    class Admin:
        pass

class ApplicantForm(ModelForm):
    email2 = forms.EmailField(label="Confirmar E-mail", help_text="Favor confirmar seu E-mail")
    
    def clean_email2(self):
        email2_value = self.data['email2']
        email_value = self.data['email']
        if not email2_value == email_value:
            raise forms.ValidationError('Os E-mails providenciados não são iguais, favor verificar a informação')
    
    def clean_birthdate(self):
        birthdate = self.cleaned_data['birthdate']
        age = calculate_age(birthdate)
        if age < 30:
            raise forms.ValidationError('Pela data de nascimento indicada, você não tem mais de 30 anos de idade. Infelizmente, no momento não estamos aprovando bolsas para pessoas com menos de 30 anos de idade. Se a data de nascimento foi preenchida incorretamente, favor corrigir a informação e prosseguir')
        return birthdate
    
    class Meta:
        model = Applicant

def calculate_age(born):
    """Calculate the age of a user."""
    from datetime import date
    today = date.today()
    try:
        birthday = date(today.year, born.month, born.day)
    except ValueError:
        # Raised when person was born on 29 February and the current
        # year is not a leap year.
        birthday = date(today.year, born.month, born.day - 1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year



SPOUSE_EMPLOYED_CHOICES = (('1', 'Sim'), ('0', 'Não'))

class ApplicantPast(models.Model):
    """An ApplicantPast is information about the individuals past education"""

    session = models.OneToOneField(ApplicationSession, editable=False)
    
    church_calling = models.CharField("Seu chamado atual na Igreja", max_length=100, help_text="Favor informar o seu chamado atual")
    other_church_calling = models.CharField("Outros cargos que ocupou na Igreja", max_length=200, blank=True)
    mission = models.CharField("Missão (se serviu) e datas (mês/ano)", max_length=100, blank=True)
    mission_start_date = models.DateField("Missão a data de início", blank=True)
    mission_end_date = models.DateField("Missão data final", blank=True)
    
    casp_date = models.DateField("Datas em que foram realizados os cursos", help_text="Favor informar a data que você concluiu o curso CASP")
    casp_instructor_name = models.CharField("Nome do Instrutor", max_length=100, help_text="Favor informar o nome do instrutor do curso CASP")
    casp_instructor_phone = models.CharField("Telefone", max_length=15, blank=True, help_text="Favor informar o nome do instrutor do curso CASP")
    
    sei_date = models.DateField("Datas em que foram realizados os cursos", help_text="Favor informar a data que você concluiu o curso Planejar Para o Sucesso")
    sei_instructor_name = models.CharField("Nome do Instrutor", max_length=100, help_text="Favor informar o nome do instrutor do curso Planejar Para o Sucesso")
    sei_instructor_phone = models.CharField("Telefone", blank=True, max_length=15)
    
    employer = models.CharField("Meu trabalho atual", max_length=100, blank=True, help_text="Favor informar o seu trabalho atual")
    salary = models.IntegerField("Remuneração mensal (não ponha centavos)", blank=True, help_text="Favor informar a sua remuneração mensal", null=True)
    
    spouse_employed = models.BooleanField("O seu cônjuge trabalha ou tem alguma renda mensal? (Caso sim, por favor indique em que trabalha no campo abaixo)", choices=SPOUSE_EMPLOYED_CHOICES)
    spouse_employer = models.CharField(max_length=100, blank=True, help_text="Favor informar o trabalho atual do seu cônjuge")
    spouse_salary = models.IntegerField("Remuneração mensal do seu cônjuge (não ponha centavos)", blank=True, help_text="Favor informar o valor da remuneração mensal do seu cônjuge", null=True)
    
    class Admin:
        pass

class ApplicantPastForm(ModelForm):

    def clean_spouse_employer(self):
        return validates_presence_of_condition(self, 'spouse_employed', 'spouse_employer', 'Favor informar o trabalho atual do seu cônjuge')

    def clean_spouse_salary(self):
        return validates_presence_of_condition(self, 'spouse_employed', 'spouse_salary', 'Favor informar o valor da remuneração mensal do seu cônjuge')
        
    class Meta:
        model = ApplicantPast



def validates_presence_of_condition(instance, condition, target, message):
    condition2 = instance.cleaned_data[condition]
    target2 = instance.data[target]
    if condition2 and not target2:
        # do i need to check for string length on target?
        raise forms.ValidationError(message)
    return instance.cleaned_data[target]


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
    def clean_program_duration(self):
        d = self.cleaned_data['program_duration']
        if (d > 24):
            raise forms.ValidationError('Pela informação indicada no campo "Duração do programa" você indicou que o curso passa o limite de 24 meses. Infelizmente nós não oferecemos bolsas para curos que tenham uma duração maior do que 24 meses.')
        return d
    class Meta:
        model = ApplicantSchool




class ApplicantCommitments(models.Model):

    session = models.OneToOneField(ApplicationSession, editable=False)

    commitment_moving_foward = models.BooleanField("Me comprometo a cumprir a filosofia Passar Adiante")
    commitment_own_money = models.BooleanField("Usarei meu próprio dinheiro para pagar tanto quanto me for possível dos custos do meu curso")
    commitment_good_student = models.BooleanField("Esforçar-me-ei ao máximo para tirar boa notas, frequentar todas as aulas, e aprender todo o material")
    commitment_faith = models.BooleanField("Permanecerei ativo na Igreja e digno de possuir uma recomendação ao templo")
    
    signature = models.CharField("Assinatura/Nome (em letra de forma)", max_length=150, help_text="Favor preencher o campo 'Assinatura/Nome', preenchendo o mesmo com o seu nome completo")

    date = models.DateField("Data (dia/mês/ano)", help_text="Favor informar a data")
    
    ward = models.CharField("Ala/Ramo do Candidato", max_length=100, help_text="Favor informar o nome da sua ala ou do seu ramo")
    bishop_name = models.CharField("Nome do Bispo ou Presidente de Ramo", max_length=100, help_text="Favor informar o nome do seu bispo atual")
    bishop_phone = models.CharField("Telefone", max_length=15, help_text="Favor informar um número")
                                                                                 
    additional_comments = models.TextField("Comentarios Adicionais", blank=True)
    
    class Admin:
        pass

class ApplicantCommitmentsForm(ModelForm):

    def clean_commitment_moving_foward(self):
        return raise_if_not_checked(self, 'commitment_moving_foward', 'Por favor lea e marque cada compromisso para poder prosseguir. Caso não esteja disposto a aceitar o compromisso, feche a janela do seu browser')
    
    def clean_commitment_own_money(self):
        return raise_if_not_checked(self, 'commitment_own_money', 'Por favor lea e marque cada compromisso para poder prosseguir. Caso não esteja disposto a aceitar o compromisso, feche a janela do seu browser')
    
    def clean_commitment_good_student(self):
        return raise_if_not_checked(self, 'commitment_good_student', 'Por favor lea e marque cada compromisso para poder prosseguir. Caso não esteja disposto a aceitar o compromisso, feche a janela do seu browser')
    
    def clean_commitment_faith(self):
        return raise_if_not_checked(self, 'commitment_faith', 'Por favor lea e marque cada compromisso para poder prosseguir. Caso não esteja disposto a aceitar o compromisso, feche a janela do seu browser')
    
    class Meta:
        model = ApplicantCommitments

def raise_if_not_checked(instance, element, message):
    v = instance.cleaned_data[element]
    if not v:
        raise forms.ValidationError(message)
    return v


