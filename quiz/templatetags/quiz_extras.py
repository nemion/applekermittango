from django import template
from ..models import Quiz, Question, Section, MultipleChoiceQuestion, FillInQuestion, EssayQuestion

import datetime
import inspect

register = template.Library()

@register.filter
def order_by(queryset, value):
    return queryset.order_by(value)

@register.filter
def full_name(user):
    return (str(user.first_name) + " " + str(user.last_name).upper()) or user.username

@register.filter
def duration(quiz):
    total = datetime.timedelta()
    for s in Section.objects.filter(quiz=quiz):
        total += s.time_limit
    if total.seconds > 3600:
        return ("%s hours %s minutes") % (total.seconds//3600, (total.seconds//60)%60)
    return ("%s minutes") % ((total.seconds//60)%60)

@register.filter
def sections_str(quiz):
    if len(Section.objects.filter(quiz=quiz)) == 1:
        return ("1 section")
    return ("%s sections") % (len(Section.objects.filter(quiz=quiz)))

@register.filter
def questions_str(quiz):
    total = 0
    for s in Section.objects.filter(quiz=quiz):
        for q in Question.objects.filter(section=s):
            total += 1
    return ("%s questions") % (total)

@register.filter
def section_points(section):
    return sum(q.points for q in Question.objects.filter(section=section))
    
@register.filter
def quiz_points(quiz):
    return sum(section_points(s) for s in Section.objects.filter(quiz=quiz))

@register.filter
def is_multiplechoice(question):
    return isinstance(question, MultipleChoiceQuestion)

@register.filter
def is_fillin(question):
    return isinstance(question, FillInQuestion)

@register.filter
def is_essay(question):
    return isinstance(question, EssayQuestion)

@register.filter
def sections(obj):
    if isinstance(obj, Quiz):
        return Section.objects.filter(quiz=obj).order_by('number')
    elif isinstance(obj, Section):
        return Section.objects.filter(quiz=obj.quiz).order_by('number')
