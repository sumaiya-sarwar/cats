from django.shortcuts import render
from django.views import View # <- View class to handle requests
from django.http import HttpResponse # <- a class to handle sending a type of response
from django.views.generic.base import TemplateView
from .models import Cat
from django.views.generic.edit import CreateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

# Here we will be creating a class called Home and extending it from the View class

class Home(TemplateView):
    template_name = "home.html"

class About(TemplateView):
    template_name = "about.html"
@method_decorator(login_required, name='dispatch')
class CatList(TemplateView):
    template_name = "cat_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # to get the query parameter we have to acccess it in the request.GET dictionary object        
        name = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["cats"] = Cat.objects.filter(name__icontains=name, user=self.request.user)
            context["header"] = f"Searching for {name}"
        else:
            context["cats"] = Cat.objects.filter(user=self.request.user)
            context["header"] = f"Searching for {name}"
        return context


class CatCreate(CreateView):
    model = Cat
    fields = ['name', 'img', 'des']
    template_name = "cat_create.html"
    success_url = "/cats/"
    # this will get the pk from the route and redirect to artist view
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CatCreate, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('cat_detail', kwargs={'pk': self.object.pk})

class CatDetail(DetailView):
    model = Cat
    template_name = "cat_detail.html"
        
        
class CatUpdate(UpdateView):
    model = Cat
    fields = ['name', 'img', 'des']
    template_name = "cat_update.html"
    success_url = "/cats/"

    def get_success_url(self):
        return reverse('cat_detail', kwargs={'pk': self.object.pk})

class CatDelete(DeleteView):
    model = Cat
    template_name = "cat_delete_confirmation.html"
    success_url = "/cats/"

class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit, validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("cat_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)
