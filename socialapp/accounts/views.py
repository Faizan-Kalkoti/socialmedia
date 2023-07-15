from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserSignUpForm, UserProfileForm

class SignUp(CreateView):
    template_name = 'accounts/signup.html'
    form_class = UserSignUpForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = UserProfileForm()
        return context

    def form_valid(self, form):
        profile_form = UserProfileForm(self.request.POST, self.request.FILES)
        if profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
        else:
            return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))


# Create your views here.
