from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import PostForm
from django.core.paginator import Paginator
from django.db.models import Q

def home(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=query) if query else Post.objects.all()
    paginator = Paginator(posts, 6)  # Mostra 6 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {'posts': page_obj, 'query': query})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
