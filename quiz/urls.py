from django.conf.urls import url

from . import views

app_name = 'quiz'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.list, name='list'),
    url(r'^quiz/(?P<quiz_id>\d+)/$', views.detail, name='detail'),
    url(r'^quiz/(?P<quiz_id>\d+)/end/$', views.end, name='end'),
    url(r'^quiz/(?P<quiz_id>\d+)/section/(?P<section_number>\d+)/$', views.section, name='section'),
    url(r'^quiz/(?P<quiz_id>\d+)/section/(?P<section_number>\d+)/next/$', views.next_section, name='next_section'),
    url(r'^quiz/(?P<quiz_id>\d+)/section/(?P<section_number>\d+)/submit/$', views.submit, name='submit'),
    url(r'^ajax/quiz_data/$', views.quiz_data, name='quiz_data'),
    url(r'^ajax/section_data/$', views.section_data, name='section_data'),
    url(r'^ajax/question_data/$', views.question_data, name='question_data'),
    url(r'^quiz/new/$', views.quiz_new, name='quiz_new'),
    url(r'^quiz/(?P<quiz_id>\d+)/edit/$', views.quiz_edit, name='quiz_edit'),
    url(r'^quiz/(?P<quiz_id>\d+)/delete/$', views.quiz_delete, name='quiz_delete'),
    url(r'^quiz/(?P<quiz_id>\d+)/section/new/$', views.section_new, name='section_new'),
    url(r'^quiz/(?P<quiz_id>\d+)/section/(?P<section_number>\d+)/edit/$', views.section_edit, name='section_edit'),
    url(r'^quiz/(?P<quiz_id>\d+)/section/(?P<section_number>\d+)/delete/$', views.section_delete, name='section_delete'),
    url(r'^quiz/(?P<quiz_id>\d+)/section/(?P<section_number>\d+)/question/new/m/$', views.question_new_m, name='question_new_m'),
    url(r'^quiz/(?P<quiz_id>\d+)/section/(?P<section_number>\d+)/question/new/f/$', views.question_new_f, name='question_new_f'),
    url(r'^quiz/(?P<quiz_id>\d+)/section/(?P<section_number>\d+)/question/new/e/$', views.question_new_e, name='question_new_e'),
    url(r'^question/(?P<question_id>\d+)/edit/$', views.question_edit, name='question_edit'),
    url(r'^question/(?P<question_id>\d+)/move_up/$', views.question_move_up, name='question_move_up'),
    url(r'^question/(?P<question_id>\d+)/move_down/$', views.question_move_down, name='question_move_down'),
    url(r'^question/(?P<question_id>\d+)/delete/$', views.question_delete, name='question_delete'),
    
]
