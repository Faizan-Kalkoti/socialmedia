from typing import Any, Dict
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts import models
from accounts.models import UserProfileInfo, User_pic
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


class HomePage(TemplateView):
    template_name='index.html'

class TestPage(LoginRequiredMixin, TemplateView):
    template_name= 'test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ( important to note concept )
        # user1 = User_pic.objects.get(username='hello')
        user1 = self.request.user
        user2 = UserProfileInfo.objects.get(user=user1)
        context['user1'] = user1
        context['user2'] = user2
        return context


class ThanksPage(TemplateView):
    template_name='thanks.html'

@login_required
def myview(request): 
    user1 = User_pic.objects.get(username='hello')
    user = UserProfileInfo.objects.get(user=user1)

    context = {'user': user, 'user1':user1}  # Create a context dictionary
    return render(request, 'vew.html', context)
    # return redirect('myview', context)