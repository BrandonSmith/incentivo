# -*- coding: utf-8 -*-

from django.db import models


class Program(models.Model):

    program_id = models.CharField(max_length=25, primary_key=True)
    program = models.CharField(max_length=25)
    
    def __unicode__(self):
        return "%s" % (self.program)


class FAQ(models.Model):
    
    question = models.CharField(max_length=500)
    answer = models.TextField()
    program = models.ForeignKey(Program)

    def __unicode__(self):
        return "%s" % (self.question)

