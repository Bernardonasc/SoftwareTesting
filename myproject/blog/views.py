from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.db.models import Q

def custom_404_view(request, exception):
    return render(request, '404.html', {})

def custom_500_view(request):
    return render(request, '500.html', {})

def home(request):
    query = request.GET.get('q')
    order = request.GET.get('order', 'created_at')
    if query:
        posts = Post.objects.filter(title__icontains=query).order_by(order)
    else:
        posts = Post.objects.all().order_by(order)
    return render(request, 'blog/home.html', {'posts': posts, 'query': query, 'order': order})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
