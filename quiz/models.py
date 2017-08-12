# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel

# Create your models here.
import time, datetime


class CurrentlyAvailableManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return super(CurrentlyAvailableManager, self).get_queryset().filter(start_date__lte=now, end_date__gte=now)
    
    
class Quiz(models.Model):
    quiz_title = models.CharField(max_length=100)
    quiz_description = models.CharField(max_length=250)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    objects = models.Manager() # The default manager.
    currently_available = CurrentlyAvailableManager()
    
    def __str__(self):
        return self.quiz_title

    
class Section(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    number = models.IntegerField()
    section_title = models.CharField(max_length=100)
    section_description = models.CharField(max_length=250)
    time_limit = models.DurationField(default=datetime.timedelta(minutes=1))
    
    class Meta:
        unique_together = ('quiz', 'number',)
    
    def __str__(self):
        return self.section_title
    
    
class Question(PolymorphicModel):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    number = models.IntegerField()
    question_text = models.TextField()
    points = models.IntegerField()
    
    class Meta:
        unique_together = ('section', 'number',)
    
    def __str__(self):
        return self.question_text
    
    
class MultipleChoiceQuestion(Question):
    pass
    

class FillInQuestion(Question):
    solution = models.CharField(max_length=50)
    
    
class EssayQuestion(Question):
    max_characters = models.IntegerField(default=300)
    
    
class Choice(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=250)
    correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.choice_text
    
    
class Result(models.Model):
    participant = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    points = models.IntegerField()
    score = models.DecimalField(decimal_places=2, max_digits=5)
    final_score = models.BooleanField(default=True)
    duration = models.DurationField()
    date_taken = models.DateTimeField()
    answers = models.TextField(default="")
    
    class Meta:
        unique_together = ('participant', 'section',)
    
    def __str__(self):
        return ("%s (%s - %s: %s)") % (self.participant, self.section.quiz, self.section, self.score)

    