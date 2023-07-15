from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.contrib import messages
from django.views.generic import (CreateView, RedirectView,
                                  ListView, DetailView, DeleteView)

from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from braces.views import SelectRelatedMixin
from posts import models
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()




class PostList(SelectRelatedMixin, ListView):
    model = models.Post
    select_related = ('user','group')


class LikedPost(SelectRelatedMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
         return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})
    
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=self.kwargs.get("pk"))
        try:
            models.PostLike.objects.create(post=post, user = self.request.user)
        except IntegrityError:
            messages.warning(self.request,("You have already liked this post!"))
        else:
            messages.success(self.request,"shup up some error occured!.")
        return super().get(request, *args, **kwargs)

class UserPosts(ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact = self.kwargs.get('username'))
        except:
            User.DoesNotExist
            raise Http404
        else:  
            return self.post_user.posts.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, DetailView):
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
       queryset =  super().get_queryset()
       return queryset.filter(user__username__iexact = self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, CreateView):
    fields =('message', 'group')
    select_related = ('user', 'group')
    model = models.Post

    def form_valid(self,form):
        self.object = form.save(commit =False)
        self.object.user =  self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)
    
    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted!')
        return super().delete(*args, **kwargs)
    

    
