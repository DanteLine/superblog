from django.db.models import F, Sum, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from blog.models import Post, Author, PostComment, MyTag, Category
from blog.forms import PostCommentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator


class HomeListView(ListView):
    template_name = 'blog/index.html'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.annotate(cnt_comment=Count('postcomment')).select_related('author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_author'] = Author.objects.annotate(all_views=Sum('post__views')).order_by('-all_views').first()
        context['most_popular_posts'] = Post.objects.order_by('-views')[:3].annotate(cnt_comment=Count('postcomment')).select_related('category').select_related('author')
        context['popular_posts'] = Post.objects.order_by('-views')[3:6]
        context['popular_tags'] = MyTag.objects.annotate(views=Sum('post__views')).annotate(cnt=Count('post')).order_by(
            '-views', '-cnt')[:20]
        return context


class AuthorDetailView(DetailView):
    template_name = 'blog/single-author.html'
    # model = Author

    def get_queryset(self):
        return Author.objects.filter(slug=self.kwargs['slug'])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.post_set.annotate(cnt_comment=Count('postcomment'))
        context['author_categories'] = Category.objects.filter(id__in=self.object.post_set.values_list('category__id'))
        context['author_tags'] = MyTag.objects.filter(id__in=self.object.post_set.values_list('tags__id'))
        return context

def post_detail(request, slug=None):
    object = get_object_or_404(Post, slug=slug)
    tags = object.tags.all()
    comments = len(object.postcomment_set.all())

    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            the_post_comment = PostComment()
            the_post_comment.user = User.objects.get(username=request.user.username)
            the_post_comment.context = form.cleaned_data['context']
            the_post_comment.post = object
            the_post_comment.save()
            messages.success(request, 'Вы оставили коментарий')
            return redirect(object)
    else:
        object.views = F('views') + 1
        object.save()
        object.refresh_from_db()
        form = PostCommentForm()
    return render(request, 'blog/single-post.html', {'form': form,
                                                     'object': object,
                                                     'tags': tags,
                                                     'comments': comments,
                                                     }
                  )


class CategoryListView(ListView):
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        posts = (
            category.post_set
            .annotate(cnt_comment=Count('postcomment'))
            .select_related('author')
            .prefetch_related('tags')
        )
        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        popular_author = (
            self.object_list
            .values('author')
            .annotate(sum_views=Sum('views'))
            .order_by('-sum_views')
            .first()
        )
        context['popular_author'] = Author.objects.get(pk=popular_author['author'])
        context['popular_posts'] = self.object_list.order_by('-views')[:3]
        context['category'] = self.object_list.first().category
        return context


def tag_search(request, slug=None):
    tag = get_object_or_404(MyTag, slug=slug)
    posts = tag.post_set.annotate(cnt_comment=Count('postcomment')).select_related('author')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/search.html', {'object_list': posts,
                                                'keyword_search': f'Поиск по тегу: {tag}',
                                                'page_obj': page_obj}
                  )


def search(request):
    keyword_search = request.GET['q']
    posts = (
        Post.objects.filter(title__icontains=keyword_search)
        .annotate(cnt_comment=Count('postcomment'))
        .select_related('author')
    )
    if posts:
        return render(request, 'blog/search.html', {'object_list': posts,
                                                    'keyword_search': f'Поисковой запрос: {keyword_search}'
                                                    }
                      )
    return render(request, 'failed_to_find.html', {'keyword_search': keyword_search})
