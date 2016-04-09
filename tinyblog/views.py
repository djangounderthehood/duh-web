from django.http import Http404
from django.shortcuts import render

from .models import Post


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'tinyblog/index.html', {'posts': posts})


def post_detail(request, slug):
    post = Post.objects.get(slug)
    if not post:
        raise Http404('No post with slug: %s' % slug)

    return render(request, 'tinyblog/article.html', {'post': post})
