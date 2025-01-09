import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db import IntegrityError

from .forms import CommentForm, LinkForm, RegistrationForm
from .models import Link, Save, Report, Profile
from taggit.models import Tag
from django.db.models import Count


def index(request):
    tags = Tag.objects.annotate(num_times=Count('link')).filter(num_times__gt=0).order_by('-num_times')[:50]
    return render(request, 'index.html', {'tags': tags})


def link_view(request, pk):
    # to-do: explore performance with DJDT, might be worth it to just get rid of num_times
    # to-do: possibly rename to link_page
    link = Link.objects.prefetch_related('tags').get(pk=pk)
    tags = Tag.objects.annotate(num_times=Count('link')).order_by('-num_times').filter(link__id=pk)
    comments = link.comments.all()[::-1]
    return render(request, 'link_view.html', {'link': link, 'tags': tags, 'comments': comments})


def filter_links(request, *args, **kwargs):
    tag = request.GET.get("tag")
    language = request.GET.get("language")
    links = Link.objects.order_by('-created_at')
    if tag:
        links = links.filter(tags__name=tag)
    if language:
        links = links.filter(language__name=language)
    return render(request, 'filter_links.html', {'links': links, 'tag': tag, 'language': language})


def user_page(request, pk):
    # to-do: decide whether to move link authorship to Profile model
    user = Profile.objects.filter(pk=pk).first()
    return render(request, 'user_page.html', {'user': user})


@login_required(login_url='/accounts/login/')
def add_comment(request, pk):
    link = get_object_or_404(Link, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.link = link
            comment.author = request.user
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
            if not link.link.startswith('https://'):
                link.link = 'https://' + link.link
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


def custom_logout(request):
    if request.method == 'GET':
        logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = form.save()
            profile = Profile()
            profile.id = account.id
            profile.user = account
            profile.name = account.username
            profile.avatar_url = 'https://cataas.com/cat'
            profile.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
