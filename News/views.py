from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, response
from .models import Post 
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import requests

url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=c15d9a18fa4f4347a6589a7ca55ef0f1')
response = requests.get(url)



# Create your views here.
def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request,'News/home.html',context)            

class PostListView(ListView):
    model = Post
    template_name = 'News/home.html'            #<app>/<model>_<viewtype>.html   -- > default route for class views to look for templates
    context_object_name = 'posts'
    ordering =['-date_posted']
    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name = 'News/user_post.html'            #<app>/<model>_<viewtype>.html   -- > default route for class views to look for templates
    context_object_name = 'posts'
    ordering =['-date_posted']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        #return super().get_queryset()





class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    fields=['title','content']

    def form_valid(self, form): 
        form.instance.author = self.request.user
        return super().form_valid(form)

    success_url = '/blog'

class PostUpdateView(LoginRequiredMixin ,UserPassesTestMixin, UpdateView):
    model = Post
    fields=['title','content']

    def form_valid(self,form): 
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    

class PostDeleteView(LoginRequiredMixin ,UserPassesTestMixin, DeleteView): #?login required and all that needs to be at the left of delete view
    model = Post 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    success_url='/blog' 
  

def about(request):
    if request.method == 'GET':
        # Code for GET requests

        # Code for POST requests
        articles = response.json()['articles']
        print(articles)
        return render(request,'News/about.html', {"articles":articles,"length":len(articles)} )

    elif request.method == 'POST':
        return render(request,'News/newspost.html',{
            "title":request.POST.get("title"),
            "image":request.POST.get("image"),
            "content":request.POST.get("content"),
            "date":request.POST.get("date"),
        })

def root(request):
    return render(request,'News/landingpage.html')