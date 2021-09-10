from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id') #  сортируем, еще можно через ordering = ['-id']
    paginate_by = 3 # поставим постраничный вывод в n-элемент

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs) # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context['filter']= PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostListSearch(ListView):
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

