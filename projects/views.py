from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Review, Tag 
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects
from devsearch.utils import paginateQuerySet
from django.conf import settings

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateQuerySet(request, projects, 3)

    context = { 'querySet':projects, 'search_query':search_query, 'custom_range': custom_range }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    formReview = ReviewForm()

    if request.method == 'POST':
        formReview = ReviewForm(request.POST)
        if formReview.is_valid():
            review = formReview.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()
            # Update project votecount
            projectObj.getVoteCount

            messages.success(request,'You review was successfully submittted!')
            return redirect('project', pk=projectObj.id)

    return render(request, 'projects/single-project.html', {'project':projectObj, 'formReview':formReview})

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(', ',',').split(',')
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit = False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {'form':form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(', ',',').split(',')
        #print('DATA', newtags)

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                if (tag is not None and tag != ''):
                    tag, created = Tag.objects.get_or_create(name=tag.strip())
                    project.tags.add(tag)

            return redirect('update-project', pk=project.id)

    context = {'form':form,'project':project,'BASE_DIR': settings.CUSTOM_BASE_DIR,}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {'object':project}
    return render(request, 'delete_template.html', context)