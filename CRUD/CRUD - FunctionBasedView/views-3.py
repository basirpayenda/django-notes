from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.sessions.models import Session

def home(request):
    queryset = Blog.objects.filter(featured=True).order_by('-created_at')
    latest = Blog.objects.filter(featured=True).order_by('-created_at')[0:6]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 4)

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    context = {
        'blogs': blogs,
        'latest': latest,
        'title':'home',
        # 'views': blog_view_num
    }
    return render(request, 'blogs/home.html', context)

def blogs(request):
    queryset = Blog.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 5)

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    context = {
        'blogs':blogs,
        'title':'blogs list'
    }
    return render(request, 'blogs/blogs.html', context)


def blog_detail(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    session_key = 'blog_views_{}'.format(blog.slug)
    if not request.session.get(session_key):
        blog.blog_views += 1
        blog.save()
        request.session[session_key] = True

    return render(request, 'blogs/blog-detail.html', {'blog':blog})


@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            slug = form.instance.slug
            form.save()
            return redirect('/')
    form = BlogForm()
    context = {
        'form':form,
    }
    return render(request, 'blogs/form.html', context)

@login_required
def blog_update(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    # if not request.user == blog.author:  # or
    if not request.user.username == blog.author.username:  # or
        print(request.user)  # basirpayenda (current logged in user)
        print(request.user.username) # basirpayenda
        print(blog.author)  # admin
        print(blog.author.username) # admin
        raise PermissionDenied

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('/')

    form = BlogForm(instance=blog)
    context= {
        'form': form
    }
    return render(request, 'blogs/form.html', context)

@login_required
def blog_delete(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    if not request.user == blog.author:
        raise PermissionDenied

    if request.method == 'POST':
        blog.delete()
        return redirect('/')
    return render(request, 'blogs/blog-delete.html', {'blog':blog})


def search_view(request):
    queryset = Blog.objects.all()
    q = request.GET.get('q')

    if q:
        queryset = queryset.filter(Q(title__icontains=q)|Q(overview__icontains=q))

    context = {
        'results':queryset,
        'query':q
    }
    return render(request, 'blogs/search-results.html', context)
