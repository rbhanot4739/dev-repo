from django.shortcuts import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CreatePost
from .models import Post


# Create your views here.
def post_list(request):
    obj = Post.objects.all()
    context = {
        'obj': obj
    }
    return render(request, "posts/list.html", context)


@login_required
def post_create(request):
    if request.POST:
        form = CreatePost(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post created successfully.')
            return redirect('post-home')
    form = CreatePost()
    return render(request, "posts/create.html", {'form': form, 'operation': 'create'})


def post_detail(request, pid):
    obj = Post.objects.get(pk=pid)
    context = {'obj': obj}
    return render(request, "posts/detail.html", context)


def post_update(request, pid):
    obj = Post.objects.get(pk=pid)
    if request.POST:
        form = CreatePost(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect(reverse("post-detail", args=(pid,)))
    form = CreatePost(instance=obj)
    return render(request, "posts/create.html", {'form': form, 'operation': 'update'})


def post_delete(request, pid):
    post = Post.objects.get(pk=pid)
    post.delete()
    return redirect('post-home')
