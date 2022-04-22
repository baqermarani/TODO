from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView , CreateView , DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'Tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        contaxt = super().get_context_data(**kwargs)
        contaxt['Tasks'] = contaxt['Tasks'].filter(user=self.request.user)
        contaxt['count'] = contaxt['Tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('Search-Area') or ''
        if search_input :
            contaxt['Tasks'] = contaxt['Tasks'].filter(title__icontains=search_input)
            contaxt['search_input'] = search_input
        return contaxt

class TaskDetail(LoginRequiredMixin ,DetailView):
    model = Task
    context_object_name = "Task"

class TaskCreate(LoginRequiredMixin , CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('Task')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin ,UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('Task')

class TaskDelete(LoginRequiredMixin ,DeleteView):
    model = Task
    context_object_name = "Task"
    success_url = reverse_lazy('Task')

class Login(LoginView):
    template_name = 'Todo/Login.html'
    fields = "__all__"
    redirect_authenticated_user = False
    def get_success_url(self):
        return reverse_lazy('Task')

class RegisterPage(FormView):
    template_name = "Todo/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("Task")

    def form_valid(self, form):
        user = form.save()
        if user is not None :
            login(self.request , user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("Task")
        return super(RegisterPage , self).get(*args, **kwargs)