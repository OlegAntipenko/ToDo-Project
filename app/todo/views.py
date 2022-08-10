from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins \
    import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import login
from .forms import UserCreateForm
from .models import Task, User
from .serializers import TaskSerializer, TaskUpdateSerializer, TaskCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreateForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    # paginate_by = 3
    model = Task
    context_object_name = 'tasks'
    template_name = 'todo/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todo/task.html'


class Statistics(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'stat'
    template_name = 'todo/statistics.html'

    def get_context_data(self, **kwargs):
        task = Task.objects.all().filter(user=self.request.user)
        tasks = Task.objects.all().filter(user=self.request.user).count()
        count_todo = Task.objects.filter(status='todo').filter(user=self.request.user).count()
        count_in_progres = Task.objects.filter(status='in_progres').filter(user=self.request.user).count()
        count_blocked = Task.objects.filter(status='blocked').filter(user=self.request.user).count()
        count_finished = Task.objects.filter(status='finished').filter(user=self.request.user).count()
        date_completion = 0
        for i in task:
            completion = (i.deadline - i.date_create).days
            date_completion = date_completion +completion
        date_completion = int(date_completion/tasks)

        context = {
            'tasks': tasks,
            'count_todo': count_todo,
            'count_in_progres': count_in_progres,
            'count_blocked': count_blocked,
            'count_finished': count_finished,
            'date_completion': date_completion
        }
        return context


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'todo/profile.html'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'job_title', 'email']
    success_url = reverse_lazy('tasks')


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'text', 'deadline']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'text', 'status', 'priorities', 'importance', 'deadline']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'todo/task_delete.html'


class TaskCreateViewSet(CreateModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(**{'user': self.request.user})


class TaskListViewSet(ListModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['title']


class TaskUpdateViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated]

    @action(http_method_names=['POST'], detail=True)
    def set_as_todo(self, request, pk=None):
        task = self.get_object()
        task.status = 'todo'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(http_method_names=['POST'], detail=True)
    def set_as_in_progres(self, request, pk=None):
        task = self.get_object()
        task.status = 'in_progres'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(http_method_names=['POST'], detail=True)
    def set_as_in_blocked(self, request, pk=None):
        task = self.get_object()
        task.status = 'blocked'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(http_method_names=['POST'], detail=True)
    def set_as_finished(self, request, pk=None):
        task = self.get_object()
        task.status = 'finished'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)


class TaskDeleteViewSet(RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
