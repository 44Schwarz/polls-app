from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
# from django.template import RequestContext, loader

from .models import Question, Choice

# Create your views here.


def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    context = {'latest_questions': latest_questions}
    # output = ', '.join(q.question_text for q in latest_questions)

    # return HttpResponse(template.render(context))
    return render(request, 'polls/index.html', context)  # returns object HttpResponse


def detail(request, question_id):
    # try:
    #     my_question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    my_question = get_object_or_404(Question, pk=question_id)
    # return HttpResponse("This is the detailed view of the question %s" % question_id)
    return render(request, 'polls/detail.html', {'question': my_question})


def results(request, question_id):
    my_question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': my_question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question,
                                                     'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def ip(request):
    user_ip = request.META.get('HTTP_X_REAL_IP')
    if user_ip is None:
        user_ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(''' <html>
                                <title>IP</title> 
                                <body>Your IP is <strong>%s</strong></body>
                            </html>''' % user_ip)
