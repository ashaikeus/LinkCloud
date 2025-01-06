from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db import IntegrityError

from .forms import CommentForm, LinkForm
from .models import Link, Save, Report
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

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def create_link(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.created_at = timezone.now()
            link.author = request.user
            link.save()
            form.save_m2m()
            return redirect('link_view', pk=link.pk)
    else:
        form = LinkForm()
    return render(request, 'create_link.html', {'form': form})

@login_required(login_url='/accounts/login/')
def save_link(request, pk):
    save = Save()
    save.link = get_object_or_404(Link, pk=pk)
    save.profile = request.user
    try:
        save.save()
    except IntegrityError:
        Save.objects.get(link=pk, profile=request.user).delete()
    return redirect('link_view', pk=pk)

@login_required(login_url='/accounts/login/')
def report_link(request, pk):
    report = Report()
    report.link = get_object_or_404(Link, pk=pk)
    report.profile = request.user
    try:
        report.save()
    except IntegrityError:
        # Some message about how you've already reported this link
        pass
    return redirect('link_view', pk=pk)