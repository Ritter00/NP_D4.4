from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from django.shortcuts import render
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id') #  сортируем, еще можно через ordering = ['-id']
    paginate_by = 10 # поставим постраничный вывод в n-элемент
    form_class = PostForm

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs) # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context['filter']= PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
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


class PostListSearch(ListView):
    model = Post
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id') #  сортируем, еще можно через ordering = ['-id']
    paginate_by = 5 # поставим постраничный вывод в n-элемент


    def get_filter(self):
        return PostFilter(self.request.GET, queryset= super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter' : self.get_filter(),
        }


class PostCreateView(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id= self.kwargs.get('pk')
        return  Post.objects.get(pk= id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'