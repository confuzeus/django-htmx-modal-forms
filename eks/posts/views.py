from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from eks.posts.forms import PostForm
from eks.posts.models import Post
from django_htmx.http import reswap, retarget, trigger_client_event


def list_posts(request):
    posts = Post.objects.all()
    list_only = request.GET.get("list_only", "no") == "yes"
    if list_only:
        tmpl = "_posts.html"
    else:
        tmpl = "index.html"
    return render(request, tmpl, {"posts": posts})


def post_form(request, pk=None):
    ctx = {}
    if pk is not None:
        post = get_object_or_404(Post, pk=pk)
        ctx["action_url"] = post.edit_url
        ctx["modal_title"] = "Edit post"
    else:
        post = None
        ctx["action_url"] = reverse_lazy("add-post")
        ctx["modal_title"] = "Post something"
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response = trigger_client_event(response, "posts:update", after="swap")
            return trigger_client_event(response, "modal:close", after="swap")
        else:
            ctx["form"] = form
            response = render(request, "_post_form.html", ctx)
            response = reswap(response, "outerHTML")
            return retarget(response, "[data-post-form]")
    else:
        form = PostForm(instance=post)
    ctx["form"] = form
    response = render(request, "post_form_modal.html", ctx)
    return trigger_client_event(response, "modal:show", after="swap")
