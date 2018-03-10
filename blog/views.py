from django.shortcuts import render

from django.http import HttpResponse

from .models import Post, Category, Tag

from django.shortcuts import get_object_or_404

import markdown

from comments.forms import CommentForm

from django.views import generic

from .helper import ListViewPage

from django.db.models import Q

# Create your views here.


# def index(resquest):
#     return HttpResponse("欢迎访问我的博客首页!")

# def index(request):
#     base = settings.BASE_DIR
#     context = {
#         'title': '我的博客首页',
#         'welcome': '欢迎访问我的博客首页',
#     }
#     return render(request, 'blog/index.html', context)

# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     context = {
#             'post_list': post_list,
#         }
#     return render(request, 'blog/index.html', context)

class IndexView(ListViewPage):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 3





# def detail(request, pk):
#     post = get_object_or_404(Post, id=pk)
#     context = {
#         'post': post,
#     }
#     return render(request, 'blog/detail.html', context)

# def detail(request, pk):
#     post = get_object_or_404(Post, id=pk)
#     post.views += 1
#     post.save(update_fields=['views'])
#     post.body = markdown.markdown(post.body, extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#     ])
#     comment_list = post.comment_set.all().order_by('-created_time')
#     context = {
#         'post': post,
#         'form': CommentForm,
#         'comment_list': comment_list,
#     }
#     # context = {
#     #     'post': post,
#     # }
#     return render(request, 'blog/detail.html', context)

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    # get方法
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views()

        return response
    # 获取当前对象
    # def get_object(self, queryset=None):
    #     post = super(PostDetailView, self).get_object(queryset=None) # 调用父类方法添加功能,(重写,再返回)
    #     post.body = markdown.markdown(post.body,extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         'markdown.extensions.toc',
    #     ])
    #     return post
    # 添加文章目录功能
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None) # 调用父类方法添加功能,(重写,再返回)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
    	context = super(PostDetailView, self).get_context_data(**kwargs)
    	form = CommentForm()
    	comment_list = self.object.comment_set.all()
    	context.update({'form': form, 'comment_list': comment_list})
    	return context

# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#     created_time__month=month
#     ).order_by('-created_time')
#     return render(request, 'blog/index.html',context={'post_list': post_list})
class ArchivesView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self, **kwargs):
        return super(ArchivesView,self).get_queryset.filter(created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month')
            ).order_by('-created_time')


class CategoryView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(ListViewPage):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # paginator = context.get('paginator')
        # page = context.get('page_obj')
        # is_paginated = context.get('is_paginated')
        # pagination_data = pagination_datas(context)

        # context.update(pagination_data)
        # return context
        test = 'test'
        data = {'test': test}
        context.update(data)
        return context

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键字'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg, 'post_list': post_list})
