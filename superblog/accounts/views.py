from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


from .forms import UserRegistrationForm, UserLoginForm, AuthorUpdateForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DeleteView
from blog.models import Author, Post, Category, MyTag
from django.contrib.auth.models import User


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')

            # Author.objects.create(user=User.objects.get(username=form.cleaned_data['username']))
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form})


def userlogin(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('lk', username)
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def simple_user(request, username=None):
    if username == request.user.username:
        user = User.objects.get(username=username)
        author = Author.objects.filter(user=user).first()
        posts = Post.objects.filter(author=author).annotate(cnt_comment=Count('postcomment'))

        return render(request, 'accounts/only_user.html', {
            'object': object,
            'author': author,
            'posts': posts
        })
    else:
        raise Http404



def update_user_author(request, username=None):
    if request.user.username == username:
        user = get_object_or_404(User, username=username)
        author = Author.objects.filter(user=user)
        if author:
            if request.method == 'POST':
                form = AuthorUpdateForm(request.POST, request.FILES, instance=author.first())
                if form.is_valid():
                    form.save()
                    return redirect('lk', username)
            else:
                form = AuthorUpdateForm(instance=author.first())
                return render(request, 'accounts/user_to_author.html', {'form': form})
        else:
            if request.method == 'POST':
                form = AuthorUpdateForm(request.POST, request.FILES)
                if form.is_valid():
                    Author.objects.create(
                        user=user,
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        author_photo=form.cleaned_data['author_photo'],
                        about=form.cleaned_data['about']
                    )
                    return redirect('lk', username)
            else:
                form = AuthorUpdateForm()
                return render(request, 'accounts/user_to_author.html', {'form': form})

    else:
        raise Http404



# def add_tags(tags_str):
#     tags = list()
#     for i in tags_str.split(','):
#         obj, created = MyTag.objects.get_or_create(title=i.strip().lower())
#         tags.append(obj)
#     return tags


def add_post(request):
    author = Author.objects.filter(user=request.user)
    if author:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                some_post = Post.objects.create(
                    title=form.cleaned_data['title'],
                    author=author.first(),
                    content=form.cleaned_data['content'],
                    photo=form.cleaned_data['photo'],
                    category=form.cleaned_data['category'],
                    tags_str=form.cleaned_data['tags_str'],
                )
                some_post.add_tags()
                return redirect(some_post)
        else:
            form = PostForm()
    else:
        return redirect('lk', request.user.username)
    return render(request, 'accounts/add_post.html', {'form': form})

def postupdate(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            post.add_tags()
        return redirect(post)

    form = PostForm(instance=post)

    return render(request, 'accounts/update_post.html', {'form': form, 'post': post})

def postdelete(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if post.author.user == request.user:
        post.delete()
        return redirect('lk', request.user.username)
    else:
        raise Http404
    # return render(request, 'accounts/only_user.html', {'object': User.objects.get(username=request.user.username)})
