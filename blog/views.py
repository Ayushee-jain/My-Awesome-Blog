from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
# UserPassesTestMixin -> we are also able to update other users post so for avoiding that we use this.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

def index(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/index.html',context)

class PostListView(ListView):
    model=Post
    template_name='blog/index.html' # <app>/<model>_<viewtype>.html 
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=8

class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html' # <app>/<model>_<viewtype>.html 
    context_object_name='posts'
    paginate_by=10
 
    # for user associated with username
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin ,CreateView):
    model=Post
    fields=['title','content']

    # setting author
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form) #validate the form
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model=Post
    fields=['title','content']

    # setting author
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form) #validate the form

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    success_url='/blog/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request,'blog/about.html')