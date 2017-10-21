from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .models import Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .forms import CommentForm
from django.shortcuts import redirect
#from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        #form.fields['text'].label = "Ваш комментарий"
        #form.fields['text'].label = "Ваш комментарий"
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.published_date = timezone.now()
            comment.save()
    form = CommentForm()
    form.fields['text'].label = "Ваш комментарий"
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
