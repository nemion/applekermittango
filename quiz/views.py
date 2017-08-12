# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404, Http404
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from dateutil import parser
from datetime import timedelta
import re

from .models import *

def index(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    return render(request, 'quiz/index.html')


@login_required
def list(request):
    if request.user.is_staff:
        quiz_list = Quiz.objects.all()
    else:
        quiz_list = Quiz.currently_available.all()
        print quiz_list
    return render(request, 'quiz/list.html', {'quiz_list': quiz_list})


@login_required
def detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz/detail.html', {'quiz': quiz})


@login_required
def section(request, quiz_id, section_number):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if section_number != '0':
        try:
            section = Section.objects.get(quiz=quiz, number=section_number)
            if Result.objects.filter(participant=request.user, section=section).exists():
                return render(request, 'quiz/section.html', {
                    'section': section,
                    'error_message': {
                        'title': 'An error occured',
                        'content': 'You have completed this section!'
                    },
                })
            if section.number != 1 and not Result.objects.filter(Q(participant=request.user) | Q(section__in=[s for s in Section.objects.filter(quiz=quiz) if s.number<section.number])):
                return render(request, 'quiz/section.html', {
                    'section': section,
                    'error_message': {
                        'title': 'Forbidden',
                        'content': 'You have not completed the previous section(s)!' 
                    },
                })
        except ObjectDoesNotExist:
            raise Http404
        return render(request, 'quiz/section.html', {'section': section})
    else:
        return render(request, 'quiz/section.html')

def next_section(request, quiz_id, section_number):
    try:
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        section = Section.objects.get(quiz=quiz, number=section_number)
        next_section = Section.objects.filter(quiz=quiz).order_by('number')[section.number]
        return HttpResponseRedirect(reverse('quiz:section', args=(quiz.id, next_section.number)))
    except IndexError:
        return HttpResponseRedirect(reverse('quiz:end', args=(quiz.id,)))

    
@login_required
def end(request, quiz_id):
    return render(request, 'quiz/end.html')


@staff_member_required
def quiz_data(request):
    if request.is_ajax():
        quiz_id = request.GET.get('id', None)
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        data = {
            'quiz_title': quiz.quiz_title,
            'quiz_description': quiz.quiz_description,
            'start_date': quiz.start_date.date(),
            'start_date_time': quiz.start_date.time(),
            'end_date': quiz.end_date.date(),
            'end_date_time': quiz.end_date.time()
        }
        return JsonResponse(data)
    else:
        raise Http404


@staff_member_required
def section_data(request):
    if request.is_ajax():
        section_id = request.GET.get('id', None)
        section = get_object_or_404(Section, pk=section_id)
        data = {
            'number': section.number,
            'section_title': section.section_title,
            'section_description': section.section_description,
            'total_minutes': section.time_limit.total_seconds()/60
        }
        return JsonResponse(data)
    else:
        raise Http404


@staff_member_required
def question_data(request):
    if request.is_ajax():
        question_id = request.GET.get('id', None)
        question = get_object_or_404(Question, pk=question_id)
        data = {
            'question_text': question.question_text,
            'points': question.points
        }
        if isinstance(question, MultipleChoiceQuestion):
            choices = [{'id': c.id, 'choice_text': c.choice_text, 'correct': c.correct} for c in Choice.objects.filter(question=question)]
            data['choices'] = choices
        elif isinstance(question, FillInQuestion):
            data['solution'] = question.solution
        elif isinstance(question, EssayQuestion):
            data['max_characters'] = question.max_characters
        return JsonResponse(data)
    else:
        raise Http404


@staff_member_required
def quiz_edit(request, quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        quiz.quiz_title = request.POST['quiz_title']
        quiz.quiz_description = request.POST['quiz_description']
        
        start_date = parser.parse(request.POST['quiz_start_date']+'T'+request.POST['quiz_start_date_time'])
        end_date = parser.parse(request.POST['quiz_end_date']+'T'+request.POST['quiz_end_date_time'])
        
        print start_date
        print end_date
        
        quiz.start_date = start_date
        quiz.end_date = end_date
        quiz.save()
        return HttpResponseRedirect(reverse('quiz:list'))
    else:
        raise Http404

        
@staff_member_required
def quiz_new(request):
    if request.method == "POST":
        start_date = parser.parse(request.POST['quiz_start_date']+'T'+request.POST['quiz_start_date_time'])
        end_date = parser.parse(request.POST['quiz_end_date']+'T'+request.POST['quiz_end_date_time'])
        quiz = Quiz(quiz_title = request.POST['quiz_title'],
                    quiz_description = request.POST['quiz_description'],
                    start_date = start_date,
                    end_date = end_date)
        quiz.save()
        return HttpResponseRedirect(reverse('quiz:list'))
    else:
        raise Http404


@staff_member_required
def quiz_delete(request, quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        quiz.delete()
        return HttpResponseRedirect(reverse('quiz:list'))
    else:
        raise Http404


@staff_member_required
def section_edit(request, quiz_id, section_number):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        section = Section.objects.get(quiz=quiz, number=section_number)
        section.section_title = request.POST['section_title']
        section.section_description = request.POST['section_description']
        section.time_limit = timedelta(minutes=int(request.POST['section_time_hours']*60)+int(request.POST['section_time_minutes']))
        section.save()
        return HttpResponseRedirect(reverse('quiz:section', args=(quiz.id, section.number)))
    else:
        raise Http404

        
@staff_member_required
def section_new(request, quiz_id):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        section = Section(quiz = quiz,
                          number = max([s.number for s in quiz.section_set.all()])+1 if quiz.section_set.all() else 1,
                          section_title = request.POST['section_title'],
                          section_description = request.POST['section_description'],
                          time_limit = timedelta(minutes=int(request.POST['section_time_hours'])*60+int(request.POST['section_time_minutes'])))
        section.save()
        return HttpResponseRedirect(reverse('quiz:section', args=(quiz_id, section.number)))
    else:
        raise Http404

        
@staff_member_required
def section_delete(request, quiz_id, section_number):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        section = Section.objects.get(quiz=quiz, number=section_number)
        section.delete()
        return HttpResponseRedirect(reverse('quiz:section', args=(quiz.id, max([s.number for s in quiz.section_set.all()]) if quiz.section_set.all() else 0)))
    else:
        raise Http404


@staff_member_required
def question_new_m(request, quiz_id, section_number):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        section = Section.objects.get(quiz=quiz, number=section_number)
        question = MultipleChoiceQuestion(section = section,
                            number = max([q.number for q in section.question_set.all()])+1 if section.question_set.all() else 1,
                            question_text = request.POST['question_text'],
                            points = request.POST['question_points'])
        question.save()
        for post_item in sorted(request.POST.iterkeys()):
            if post_item.startswith('question'):
                match = re.match(r"question_new__choice_(?P<choice_id>(\d+))", post_item)
                if match and post_item.endswith('value'):
                    correct = True if 'question_new__choice_'+match.group('choice_id')+'_correct' in request.POST else False
                    choice = Choice(question = question,
                                    choice_text = request.POST[post_item],
                                    correct = correct)
                    choice.save()
        return HttpResponseRedirect(reverse('quiz:section', args=(quiz_id, question.section.number)))
    else:
        raise Http404

    
@staff_member_required
def question_new_f(request, quiz_id, section_number):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        section = Section.objects.get(quiz=quiz, number=section_number)
        question = FillInQuestion(section = section,
                            number = max([q.number for q in section.question_set.all()])+1 if section.question_set.all() else 1,
                            question_text = request.POST['question_text'],
                            points = request.POST['question_points'],
                            solution = request.POST['question_solution'])
        question.save()
        return HttpResponseRedirect(reverse('quiz:section', args=(quiz_id, question.section.number)))
    else:
        raise Http404
    

@staff_member_required
def question_new_e(request, quiz_id, section_number):
    if request.method == "POST":
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        section = Section.objects.get(quiz=quiz, number=section_number)
        question = EssayQuestion(section = section,
                            number = max([q.number for q in section.question_set.all()])+1 if section.question_set.all() else 1,
                            question_text = request.POST['question_text'],
                            points = request.POST['question_points'],
                            max_characters = request.POST['question_max_characters'])
        question.save()
        return HttpResponseRedirect(reverse('quiz:section', args=(quiz_id, question.section.number)))
    else:
        raise Http404


@staff_member_required
def question_edit(request, question_id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=question_id)
        question.question_text = request.POST['question_text']
        question.points = request.POST['question_points']
        
        if request.POST.get('question_solution', None):
            question.solution = request.POST['question_solution']
            
        if request.POST.get('question_max_characters', None):
            question.max_characters = request.POST['question_max_characters']
            
        question.save()

        for post_item in request.POST.iterkeys():
            if post_item.startswith('question'):
                match = re.match(r"question_(?P<question_id>(\d+))__choice_(?P<choice_id>(\d+))", post_item)
                if match and post_item.endswith('value'):
                    choice_id = match.group('choice_id')
                    choice = Choice.objects.get(pk=choice_id)
                    choice.choice_text = request.POST[post_item]
                    choice.save()
        return HttpResponseRedirect(reverse('quiz:section', args=(question.section.quiz.id, question.section.number)))
    else:
        raise Http404


@staff_member_required
def question_move_up(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        prev_question = Question.objects.get(section=question.section, number=question.number-1)
        temp_number = prev_question.number
        question.number, prev_question.number = -1, question.number
        question.save()
        prev_question.save()
        question.number = temp_number
        question.save()
    except ObjectDoesNotExist:
        pass
    
    return HttpResponseRedirect(reverse('quiz:section', args=(question.section.quiz.id, question.section.number)))


@staff_member_required
def question_move_down(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        next_question = Question.objects.get(section=question.section, number=question.number+1)
        temp_number = next_question.number
        question.number, next_question.number = -1, question.number
        question.save()
        next_question.save()
        question.number = temp_number
        question.save()
    except ObjectDoesNotExist:
        pass
    
    return HttpResponseRedirect(reverse('quiz:section', args=(question.section.quiz.id, question.section.number)))


@staff_member_required
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return HttpResponseRedirect(reverse('quiz:section', args=(question.section.quiz.id, question.section.number)))


def submit(request, quiz_id, section_number):
    if request.user != AnonymousUser:
        if request.method == "POST":
            quiz = get_object_or_404(Quiz, pk=quiz_id)
            section = Section.objects.get(quiz=quiz, number=section_number)

            if Result.objects.filter(participant=request.user, section=section).exists():
                return render(request, 'quiz/section.html', {
                    'section': section,
                    'error_message': "You have submitted your answers!",
                })

            points, final_score, answers = 0, True, ""
            for key in sorted(request.POST.iterkeys()):
                value = request.POST[key]
                if key.startswith('question'):
                    question = Question.objects.get(pk=key[9:])
                    if isinstance(question, MultipleChoiceQuestion) :
                        if Choice.objects.get(pk=value).correct:
                            answers += ("%s. %s, \n") % (question.number, Choice.objects.get(pk=value).choice_text)
                            points += question.points
                        else:
                            answers += ("%s. %s(incorrect), \n") % (question.number, Choice.objects.get(pk=value).choice_text)
                    elif isinstance(question, FillInQuestion):
                        answers += ("%s. %s, \n") % (question.number, value)
                        if question.solution.lower() == value.lower():
                            points += question.points
                    elif isinstance(question, EssayQuestion):
                        final_score = False
                        answers += ("%s. %s, \n") % (question.number, value)

            total_points = sum([q.points for q in Question.objects.filter(section=section)])
            result = Result(participant = request.user,
                            section = section,
                            points = points,
                            score = float(points)/total_points*100,
                            final_score = final_score,
                            duration = timedelta(seconds=section.time_limit.total_seconds()-int(request.POST['time_limit'])),
                            date_taken = timezone.now(),
                            answers = answers)
            result.save()
            return HttpResponseRedirect(reverse('quiz:next_section', args=(section.quiz.id, section.number)))
        else:
            raise Http404
        return render(request, 'quiz/section.html', {'quiz_id': quiz_id, 'section_id': section_id})
    else:
        error_message = {
            'title': 'Error',
            'content': 'You are logged out. Please log back in.'
        }
        return render(request, 'quiz/error.html', {'error_message': error_message})
