# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.db import models
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'number_of_votes')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    
    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Sum('choice__votes'))
        return qs
    
    def number_of_votes(self, obj):
        return obj.choice__votes__sum
    number_of_votes.admin_order_field = 'choice__votes__sum'

    
admin.site.register(Question, QuestionAdmin)