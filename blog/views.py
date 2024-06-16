# blog/views.py

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from blog.models import Post, Comment
from blog.forms import CommentForm


def blog_list(request):
    posts = Post.objects.all().order_by("-created_on")
    paginator = Paginator(posts, 5)  # Show 5 posts per page.
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
    }
    return render(request, "blog/blog.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(post=post)

    # Get the three most recent posts excluding the current post
    latest_posts = Post.objects.exclude(pk=pk).order_by('-created_on')[:3]

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "latest_posts": latest_posts,
    }

    return render(request, "blog/detail.html", context)