from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin




class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id') #  сортируем, еще можно через ordering = ['-id']
    paginate_by = 7 # поставим постраничный вывод в n-элемент
    form_class = PostForm

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs) # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context['filter']= PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request,*args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)

class PostDetail(DetailView):
    #model = Post
    #template_name = 'post.html'
    #context_object_name = 'post'
    template_name = 'post_detail.html'
    queryset = Post.objects.all()


class PostListSearch(ListView,):
    model = Post
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id') #  сортируем, еще можно через ordering = ['-id']
    paginate_by = 10 # поставим постраничный вывод в n-элемент


    def get_filter(self):
        return PostFilter(self.request.GET, queryset= super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter' : self.get_filter(),
        }


class PostCreateView(PermissionRequiredMixin,CreateView):
    template_name = 'post_create.html'
    permission_required = ('myapp.add_post', )
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    permission_required = ('myapp.change_post')
    form_class = PostForm


    def get_object(self, **kwargs):
        id= self.kwargs.get('pk')
        return  Post.objects.get(pk= id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context




class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')

