from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from .constans import POSTS_ON_PAGE
from .forms import CommentForm, PostForm
from .models import Follow, Post, Group, User


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page': page
    })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {
        'page': page,
        'group': group
    })


@login_required
def new_post(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None,)
    if not form.is_valid():
        return render(request, 'new.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    form.save()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'author': author
    }
    return render(request, 'profile.html', context=context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    author = post.author
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'author': author,
        'comments': comments,
        'form': form
    }
    return render(request, 'post.html', context=context)


@login_required
def post_edit(request, username, post_id):
    if username != request.user.username:
        return redirect('post', username=username, post_id=post_id)
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    context = {
        'form': form,
        'post': post
    }
    if not form.is_valid():
        return render(request, 'new.html', context=context)
    form.save()
    return redirect('post', username=username, post_id=post_id)


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path,
         'exeption': exception},
        status=404
    )


def server_error(request):
    return render(
        request,
        'misc/500.html',
        status=500
    )


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if not form.is_valid():
        form = CommentForm()
        return render(request, 'comments.html', {'form': form})
    comment = form.save(commit=False)
    comment.author = request.user
    comment.post = post
    form.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'posts': posts}
    return render(request, 'follow/follow.html', context)


@login_required
def profile_follow(request, username):
    follow_user = get_object_or_404(User, username=username)
    if follow_user != request.user:
        Follow.objects.get_or_create(user=request.user, author=follow_user)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username)
    _ = get_object_or_404(
        Follow,
        user=request.user,
        author=unfollow_user
    ).delete()
    return redirect('profile', username=username)
