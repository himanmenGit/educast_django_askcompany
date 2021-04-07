from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    DetailView,
    ArchiveIndexView,
    YearArchiveView,
)
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import get_object_or_404
from .models import Post
from .forms import PostForm


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect(post)
    else:
        form = PostForm()

    return render(request, 'instagram/post_form.html', {
        'form': form,
    })


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, '작성자만 수정 가능 합니다.')
        return redirect(post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post)
    else:
        form = PostForm(instance=post)

    return render(request, 'instagram/post_form.html', {
        'form': form,
    })


# post_list = login_required(ListView.as_view(model=Post, paginate_by=10))


# @method_decorator(login_required, name="dispatch")
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 100


post_list = PostListView.as_view()


# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get("q", "")

#     if q:
#         qs = qs.filter(message__icontains=q)
#     return render(
#         request,
#         "instagram/post_list.html",
#         {"post_list": qs, "q": q},
#     )


# def post_detail(reqeust: HttpRequest, pk: int) -> HttpResponse:
#     # try:
#     #     post = Post.objects.get(pk=pk)
#     # except Post.DoesNotExist:
#     #     raise Http404
#     post = get_object_or_404(Post, pk=pk)
#     return render(reqeust, "instagram/post_detail.html", {"post": post})

# post_detail = DetailView.as_view(model=Post)


class PostDetailView(DetailView):
    model = Post

    # queryset = Post.objects.filter(is_public=True)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
        return qs


post_detail = PostDetailView.as_view()

# def archives_year(request, year):
#     return HttpResponse(f"{year} Welcome")


post_archive = ArchiveIndexView.as_view(
    model=Post, date_field="created_at", paginate_by=10
)

post_archive_year = YearArchiveView.as_view(
    model=Post, date_field="created_at", make_object_list=True
)
