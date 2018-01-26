from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect

from blog.models import Post

from .models import Comment

from .forms import CommentForm
# Create your views here.

def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post)
        else:
            # comment_list = post.comment_set.all().order_by('-created_time')
            # context = {
            #     'post': post,
            #     'form': form,
            #     'comment_list': comment_list,
            # }
            # return render(request, 'blog/detail.html', context)
            return render(request, 'blog/detail.html')

    return redirect(post)
