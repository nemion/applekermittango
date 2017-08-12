# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.db import models
from .models import Quiz, Section, Question, EssayQuestion, FillInQuestion, MultipleChoiceQuestion, Choice, Result


class SectionInline(admin.StackedInline):
    model = Section
    extra = 1

    
class QuizAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['quiz_title', 'quiz_description']}),
        ('Date information', {'fields': ['start_date', 'end_date']}),
    ]
    inlines = [SectionInline]
    
    list_display = ['quiz_title']
    list_filter = ['start_date']
    search_fields = ['quiz_title']
    
    
class MultipleChoiceQuestionInline(admin.StackedInline):
    model = MultipleChoiceQuestion
    extra = 1
    
class FillInQuestionInline(admin.StackedInline):
    model = FillInQuestion
    extra = 1
    
class EssayQuestionInline(admin.StackedInline):
    model = EssayQuestion
    extra = 1
    
class SectionAdmin(admin.ModelAdmin):
    inlines = [MultipleChoiceQuestionInline, FillInQuestionInline, EssayQuestionInline]
    
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    
class ResultAdmin(admin.ModelAdmin):
    list_display = ['get_quiz', 'section', 'participant', 'score', 'duration', 'date_taken', 'final_score']

    def get_quiz(self, obj):
        return obj.section.quiz
    get_quiz.short_description = 'Quiz'
    get_quiz.admin_order_field = 'section__quiz'
    
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(Result, ResultAdmin)