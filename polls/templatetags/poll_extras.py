from django import template

register = template.Library()


import datetime
from django.utils import timezone


@register.filter
def get_percentage(question, choice):
    total_votes = sum([c.votes for c in question.choice_set.all()])
    return round(float(choice.votes)/total_votes*100, 2)

@register.filter
def limit(choice_forms, lim):
    return choice_forms[:lim]

@register.filter
def limitfrom(choice_forms, lim):
    return choice_forms[lim:]

@register.filter
def ordered(array, value):
    return array.order_by(value)

@register.filter
def get_string(date):
    now = timezone.now()
    diff = now-date
    
    """
    from: https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
    
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"
    
    