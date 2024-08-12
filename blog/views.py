from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .models import BlogCategory, BlogComment, Blog
from .forms import PubBlogForm


# Create your views here.

def index(request):
    return render(request, 'index.html')


def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    return render(request, 'blog_detail.html', context={'blog': blog})


# @login_required(login_url=reverse_lazy('xiaoauth:login'))
# @login_required(login_url=reverse_lazy('/auth/login'))

@require_http_methods(['GET', 'POST'])
@login_required()
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context={'categories': categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({'code': 200, 'message': 'Blog post successfully!', 'data': {'blog_id': blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code': 400, 'message': 'Invalid parameter'})


@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
    return redirect(reverse('blog:blog_detail', kwargs={'blog_id': blog_id}))
