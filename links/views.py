from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm
from .models import Link
from taggit.models import Tag
from django.db.models import Count


def index(request):
    tags = Tag.objects.annotate(num_times=Count('link')).filter(num_times__gt=0).order_by('-num_times')[:50]
    return render(request, 'index.html', {'tags': tags})


def link_view(request, pk):
    link = Link.objects.get(pk=pk)
    tags = link.tags.annotate(num_times=Count('link')).order_by('-num_times')
    comments = link.comments.all()
    return render(request, 'link_view.html', {'link': link, 'tags': tags, 'comments': comments})


def tag_links(request, name):
    links = Link.objects.filter(tags__name=name)
    return render(request, 'tag_links.html', {'links': links, 'tag': name})


def add_comment(request, pk):
    link = get_object_or_404(Link, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.link = link
            comment.save()
            return redirect('link_view', pk=link.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})
