# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question
from .forms import QuestionForm, ChoiceForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]
    
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def new(request):
    max_choices = 10
    if request.method == "POST":
        qform = QuestionForm(request.POST, instance=Question())
        cforms = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range (0,max_choices)]
        if qform.is_valid() and all(cf.is_valid() for cf in cforms) and cforms[0].data['0-choice_text'] and cforms[0].data['1-choice_text']:
            question = qform.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            for cf in cforms:
                if cf.data[cf.prefix + '-choice_text']:
                    choice = cf.save(commit=False)
                    choice.question = question
                    choice.save()
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
    else:
        qform = QuestionForm()
        cforms = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range (0,max_choices)]
    return render(request, 'polls/new.html', {'question_form': qform, 'choice_forms': cforms})
