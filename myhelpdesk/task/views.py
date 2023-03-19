from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from task.forms import AddTaskForm
from task.models import Task, Status


def index(request):
    tasks = Task.objects.all()
    stats = Status.objects.all()

    context = {
        'tasks': tasks,
        'stats': stats,
        'title': 'Task List',
        'stat_selected': 0,
    }

    return render(request, 'task/index.html', context=context)


class ShowTask(DetailView):
    model = Task
    template_name = 'task/task.html'
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'
    extra_context = {'title': 'Task'}


# def add_task(request):
#     if request.method == 'POST':
#         form = AddTaskForm(request.POST)
#         if form.is_valid():
#             try:
#                 Task.objects.create(**form.cleaned_data)
#                 return redirect('index')
#             except:
#                 form.add_error(None, '!! Add  task error !!')
#
#     else:
#         form = AddTaskForm()
#     return render(request, 'task/add_task.html', {'form': form, 'title': 'Add Task'})

def add_task(request):
    if request.method == 'POST':
        form = AddTaskForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                task = Task.objects.create(**form.cleaned_data)
                task.user = request.user
                task.save()
                return redirect('index')
            except:
                form.add_error(None, '!! Add task error !!')

    else:
        form = AddTaskForm(user=request.user)
    return render(request, 'task/add_task.html', {'form': form, 'title': 'Add Task'})


def show_status(request, status_id):
    tasks = Task.objects.filter(status_id=status_id)
    stats = Status.objects.all()

    if len(tasks) == 0:
        raise Http404()

    context = {
        'tasks': tasks,
        'stats': stats,
        'title': 'Status view',
        'status_selected': status_id,
    }

    return render(request, 'task/index.html', context=context)
