from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogForm


def homepage(request):
    object_list = BlogPost.objects.all()
    context = {
        'queryset': object_list
    }
    return render(request, 'blogs/home.html', context)


def blog_detail(request, title_slug):
    obj = get_object_or_404(BlogPost, slug=title_slug)
    context = {
        'obj': obj
    }
    return render(request, 'blogs/blog-detail.html', context)


def blog_create(request):
    if request.method == 'POST':
        create_form = BlogForm(request.POST, request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect('blog:home')
    create_form = BlogForm()

    context = {
        'create_form': create_form
    }
    return render(request, 'blogs/blog-form.html', context)


def blog_update(request, title_slug):
    obj = get_object_or_404(BlogPost, slug=title_slug)
    if request.method == 'POST':
        update_form = BlogForm(request.POST, request.FILES, instance=obj)
        if update_form.is_valid():
            update_form.save()
            return redirect('blog:home')
    update_form = BlogForm(instance=obj)

    context = {
        'update_form': update_form
    }
    return render(request, 'blogs/blog-update.html', context)


def blog_delete(request, title_slug):
    target_post = get_object_or_404(BlogPost, slug=title_slug)
    if request.method == 'POST':
        target_post.delete()
        return redirect('blog:home')
    
    context = {
        'target_post': target_post
    }
    return render(request, 'blogs/blog-delete.html', context)
