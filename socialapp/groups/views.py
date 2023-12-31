from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.urls import reverse
from django.urls import reverse_lazy
from groups.models import Group, GroupMember
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views.generic import (CreateView, RedirectView, 
                                  ListView, DeleteView, DetailView)
from django import forms

#To rename the labels of the model using the form class
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'g_description', 'group_img')
        labels = {
            'name': 'Group Name',
            'g_description': 'Group Description',
            'group_img': 'Group Image',
        }

class CreateGroup(LoginRequiredMixin, CreateView):
    form_class = GroupForm
    model = Group
    

class SingleGroup(DetailView):
    model = Group

class ListGroup(ListView):
    model = Group
    paginate_by = 3 

class DeleteGroup(LoginRequiredMixin, DeleteView):
    template_name = 'groups/group_delete.html'
    model = Group
    success_url = reverse_lazy('groups:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(slug = self.kwargs['slug'])
    
    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Group Deleted!')
        return super().delete(*args, **kwargs)



class JoinGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))
        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)




class LeaveGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(user=self.request.user,
                                                    group__slug=self.kwargs.get("slug")).get()
        except GroupMember.DoesNotExist:
            messages.warning( self.request,
                              "You can't leave this group because you aren't in it." )
        else:
            membership.delete()
            messages.success( self.request,
                              "You have successfully left this group." )
            
        return super().get(request, *args, **kwargs)


