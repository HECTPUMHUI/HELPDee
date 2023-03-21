from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from task.forms import AddTaskForm, CommentForm
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


def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = task
            comment.save()
            return redirect('task', task_id=task.id)
    else:
        form = CommentForm()
    return render(request, 'task/add_comment.html', {'form': form})
