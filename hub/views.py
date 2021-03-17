from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Tutorial, Curriculum
from .filters import TutorialFilter
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# class HomeView(ListView):
#     model = Tutorial
#     template_name = 'home.html'

#tutorial list test, urls
def HomeView(request):
    tutorials = Tutorial.objects.all()
    # tutorial = tutorials.tutoriallist_set.all() parent child relationship case
    myFilter = TutorialFilter(request.GET, queryset=tutorials)
    tutorials = myFilter.qs
    return render(request, 'home.html', {'tutorials': tutorials, 'myFilter': myFilter})



#243, home.html
#< button class ="btn btn-secondary reset_btn" type="submit" > < a class ="reset_btn" href="{% url 'hub:tutorial_list'%}" > Reset < / a > < / button >
#Tutorial
# def TutorialsList(request):
#     tutorials = Tutorial.objects.all()
#     # tutorial = tutorials.tutoriallist_set.all() parent child relationship case
#     myFilter = TutorialFilter(request.GET, queryset=tutorials)
#     tutorials = myFilter.qs
#     return render(request, 'tutorial_list.html', {'tutorials': tutorials, 'myFilter':myFilter})

class TutorialDetailsView(DetailView):
    model = Tutorial
    template_name = 'tutorial_detail.html'


#Register
class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


#Curriculum
@login_required
def add_to_cart(request, pk):
    tutorial = get_object_or_404(Tutorial, pk=pk)
    Curriculum.objects.get_or_create(user=request.user)
    curriculum_queryset = Curriculum.objects.filter(user=request.user)
    curriculum = curriculum_queryset[0]
    curriculum.tutorial.add(tutorial)
    messages.info(request, "Tutorial added to your curriculum")
    return redirect("hub:curriculum_summary")



@login_required
def CurriculumSummaryView(request):
    try:
        curriculum = Curriculum.objects.get(user=request.user)
        #curriculum = Curriculum.objects.filter(user=request.user) #multiple curriculums...
        context = {'curriculum': curriculum}
        return render(request, 'curriculum_summary.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "You do not have a curriculum, start by adding your first tutorial")
        return redirect("/") # CHANGE:  to tutorial list



class ProductView(DetailView):
    model = Tutorial
    template_name = 'product.html'
