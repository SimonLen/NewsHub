from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from .tasks import send_new_post_notification
from NewsHub import settings


class PostsList(ListView):
    model = Post
    ordering = '-creation_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = '-creation_date'
    template_name = 'posts_search.html'
    context_object_name = 'post_search'
    paginate_by = 2

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostAddView(PermissionRequiredMixin, CreateView):
    template_name = 'posts_modifications/post_add.html'
    form_class = PostForm
    permission_required = ('news.add_post', )

    def form_valid(self, form_class):
        post = form_class.save()
        categories = post.category.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]
        send_new_post_notification.delay(preview=post.preview(), pk=post.pk, title=post.title, subs=subscribers)
        return redirect(f'{settings.SITE_URL}/news/{post.pk}')


class PostEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'posts_modifications/post_add.html'
    form_class = PostForm
    permission_required = ('news.change_post', )

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'posts_modifications/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post', )


class CategoryPostsList(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_post_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-_rating', '-creation_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['is_not_subscribed'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = "Вы успешно подписались на рассылку новостей категории"
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
