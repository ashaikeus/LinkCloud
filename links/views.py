from django.http import HttpResponse
from django.shortcuts import render
from .models import Link
from taggit.models import Tag
from django.db.models import Count


def index(request):
    tags = Tag.objects.annotate(num_times=Count('link')).order_by('-num_times')
    return render(request, 'index.html', {'tags': tags})


def link_view(request, pk):
    link = Link.objects.get(pk=pk)
    # tags = link.tags.all()
    tags = link.tags.all().annotate(num_times=Count('link')).order_by('-num_times')
    return render(request, 'link_view.html', {'link': link, 'tags': tags})


def tag_links(request, name):
    links = Link.objects.filter(tags__name=name)
    print(links)
    return render(request, 'tag_links.html', {'links': links, 'tag': name})
