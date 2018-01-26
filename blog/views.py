from django.shortcuts import render

from django.http import HttpResponse

from .models import Post,Category

from django.shortcuts import get_object_or_404

import markdown

from comments.forms import CommentForm

from django.views import generic

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

class IndexView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        # 当前页左边连续的页码号, 初始值为空
        left = []
        # 当前页右边连续的页码号, 初始值为空
        right = []
        # 标示第一页页码后是否需要显示省略号
        left_has_more = False
        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        first = False
        # 标示是否需要显示最后一页的页码号
        last = False

        page_number = page.number

        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages -1 :
                right_has_more = True


            if right[-1] < total_pages :
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number -1]


            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:

            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number -1]
            right = page_range[page_number:page_number + 2]


            if right[-1] < total_pages - 1 :
                right_has_more = True

            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

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
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None) # 调用父类方法添加功能,(重写,再返回)
        post.body = markdown.markdown(post.body,extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
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
        return Post.objects.filter(created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month')
            ).order_by('-created_time')

class CategoryView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
