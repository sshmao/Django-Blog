"""
BlogApp的model模型
"""
import markdown
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.html import strip_tags


class Category(models.Model):
    """
    分类
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章
    """
    title = models.CharField(max_length=70)
    body = models.TextField()
    # auto_now_add(自动创建现在时间,不可修改)
    created_time = models.DateTimeField(auto_now_add=True)
    # auto_now(自动创建现在时间,可修改)
    modified_time = models.DateTimeField(auto_now=True)
    # 摘要 字符串类型 blank=true(前端验证可以为空) null=true(数据库验证可为空)
    excerpt = models.CharField(max_length=200, blank=True, null=True)
    # 阅读量 计数字段(默认为0) positiveintegerfield(正整数字段)
    views = models.PositiveIntegerField(default=0)
    # 分类外键(一对多)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 标签外键(多对多)
    tags = models.ManyToManyField(Tag, blank=True)
    # 用户外键(一对多)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ['-created_time']
    def save(self, *args, **kwargs):
        if not self.excerpt:
            # 首先实例化一个markdown类,用于渲染body的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将Markdown 文本渲染成HTML文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        else:
            self.excerpt = 'save函数自动改动的值'
        super(Post,self).save(*args, **kwargs)
