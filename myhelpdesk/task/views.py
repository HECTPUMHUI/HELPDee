from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import model_to_dict
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from task.forms import AddTaskForm, CommentForm, ReasonForm, TaskForm
from task.models import Task, Status, RestoreTask
from task.serializers import TaskSerializer
from user.models import User


class TaskListView(ListView):
    """
    give all tasks for user on main page, and all task if you admin
    """
    model = Task
    template_name = 'task/index.html'
    context_object_name = 'tasks'

    # paginate_by = 6

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = super().get_queryset().filter(hidden=False)
        else:
            queryset = super().get_queryset().filter(hidden=False, user=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = Status.objects.all()
        context['title'] = 'Task List'
        context['stat_selected'] = 0
        return context


class ShowTask(LoginRequiredMixin, DetailView):
    """
    Show a task details
    """
    model = Task
    template_name = 'task/task.html'
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'
    extra_context = {'title': 'Task'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        if task.user == self.request.user:
            if task.process == 'rejected':
                context['restore_button'] = True
        return context


def add_task(request):
    """
    this func add new task
    """
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
    """
    this func view task about status
    """
    if request.user.is_superuser:
        tasks = Task.objects.filter(status_id=status_id)
    else:
        tasks = Task.objects.filter(status_id=status_id, user=request.user.id)
    stats = Status.objects.all()

    if len(tasks) == 0:
        # if task with some status absent, we gave 404 page
        raise Http404()

    context = {
        'tasks': tasks,
        'stats': stats,
        'title': 'Status view',
        'status_selected': status_id,
    }

    return render(request, 'task/index.html', context=context)


def add_comment(request, task_id):
    """
    this task for comment under task
    """
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


# test
def task_accept(request, task_id):
    """
    func for admin, he can accept task adn task give process - accepted
    """
    task = get_object_or_404(Task, id=task_id)
    task.process = 'accepted'
    task.hidden = False
    task.save()
    return redirect('task', task_id=task_id)


def task_reject(request, task_id):
    """
        func for admin, he can reject task and task give process - rejected and add comment for reason

    """
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = ReasonForm(request.POST)
        if form.is_valid():
            task.reason = form.cleaned_data['reason']
            task.process = 'rejected'
            task.save()
            return redirect('index')
    else:
        form = ReasonForm()
    return render(request, 'task/reject.html', {'form': form})


def task_restore(request, task_id):
    """
     user can restore his task, after admin rejected task
     """
    task = get_object_or_404(Task, id=task_id)
    task.process = 'process of recovery'
    task.hidden = True
    task.save()
    RestoreTask.objects.create(task=task)
    return redirect('index')


class RestoreTaskList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    class for restored task, were admin can accept or not
    """
    model = Task
    template_name = 'task/restore_list.html'
    context_object_name = 'restored_tasks'

    # paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(hidden=True)
        return queryset


def edit_task(request, task_id):
    """
    this func add edit opportunity
    """
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task/edit_task.html', {'form': form, 'task_id': task_id})
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task', task_id)
        else:
            return render(request, 'task/edit_task.html', {'form': form, 'task_id': task_id})


# !!!!!!!!!!!!!!!!!!! REST !!!!!!!!!!!!!!!!!!!!

class TaskAPIView(APIView):
    """
    this class for output tasks with input status
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        """
        in this func we filtered data if we give a status number
        """
        status = request.query_params.get('status')
        if status:
            tasks = Task.objects.filter(status=status)
        else:
            tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskAPIList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskAPIUpdate(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
