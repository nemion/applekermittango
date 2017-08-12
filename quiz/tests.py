# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
import datetime

from django.utils import timezone
from django.test import TestCase

from .models import *

class QuizTestCase(TestCase):
    
    def setUp(self):
        q = Quiz(quiz_title='My First Quiz',
                 quiz_description='This is a demo quiz.',
                 start_date=timezone.now(),
                 end_date=timezone.now()+datetime.timedelta(days=1),
                 total_points=60)
        
        s1 = Section(quiz=q,
                     section_title='Section A',
                     section_description='This section consists of three multiple choice questions')
        
        mcq1 = MultipleChoiceQuestion(section=s1,
                                     question_text='What is the most popular fruit in the US?',
                                     time_limit=datetime.timedelta(minutes=3),
                                     points=5)
        
        mcq1c1 = Choice(question=mcq1, choice_text='Apple', correct=False)
        mcq1c2 = Choice(question=mcq1, choice_text='Orange', correct=False)
        mcq1c3 = Choice(question=mcq1, choice_text='Berry', correct=False)        
        mcq1c4 = Choice(question=mcq1, choice_text='Banana', correct=True)
        
        mcq2 = MultipleChoiceQuestion(section=s1,
                                     question_text='Which city is the most populated in the world?',
                                     time_limit=datetime.timedelta(minutes=3),
                                     points=5)
        
        mcq2c1 = Choice(question=mcq2, choice_text='Shanghai', correct=False)
        mcq2c2 = Choice(question=mcq2, choice_text='Delhi', correct=False)
        mcq2c3 = Choice(question=mcq2, choice_text='Tokyo', correct=True)        
        mcq2c4 = Choice(question=mcq2, choice_text='Mexico City', correct=False)
        
        mcq3 = MultipleChoiceQuestion(section=s1,
                                     question_text='When did Thomas Edison invent the electric light bulb?',
                                     time_limit=datetime.timedelta(minutes=3),
                                     points=5)
        
        mcq3c1 = Choice(question=mcq3, choice_text='1879', correct=True)
        mcq3c2 = Choice(question=mcq3, choice_text='1881', correct=False)
        mcq3c3 = Choice(question=mcq3, choice_text='1889', correct=False)        
        mcq3c4 = Choice(question=mcq3, choice_text='1895', correct=False)
        
        s2 = Section(quiz=q,
                     section_title='Section B',
                     section_description='This section consists of two fill in the blank questions.')
        
        fiq1 = FillInQuestion(section=s2,
                             question_text='What is WHO short for?',
                             time_limit=datetime.timedelta(minutes=3),
                             points=10,
                             solution='World Health Organization')
        
        fiq2 = FillInQuestion(section=s2,
                             question_text='When is the best time to go to the dentist?',
                             time_limit=datetime.timedelta(minutes=3),
                             points=10,
                             solution='Tooth Hurty')
        
        s3 = Section(quiz=q,
                     section_title='Section C',
                     section_description='This section consists of one essay question')
        
        esq1 = EssayQuestion(section=s3,
                             question_text='Why is the sky blue?',
                             time_limit=datetime.timedelta(minutes=15),
                             points=25,
                             max_characters=300)