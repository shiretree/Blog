from django.contrib.auth.models import User
from django.db import models


# Create your models here.



class Link(models.Model):

    STATUS_NORMAL = 1           #为啥子都要个状态呢？
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    href = models.URLField(verbose_name="链接")   #默认长度为200
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1,6),range(1,6)), verbose_name="权重",
                                         help_text="权重高的展示序列靠前")   #为什么两个range？查一下zip用法
    """
    当zip()函数有两个参数时，zip(a,b)函数分别从a和b中取一个元素组成元组，再次将组成的元组组合成一个新的迭代器。
    a与b的维数相同时，正常组合对应位置的元素。当a与b行或列数不同时，取两者中的最小的行列数。
    """
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '友链'

class SideBar(models.Model):

    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    )

    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT =3
    DISPLAY_COMMENT = 4

    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOT, '最热文章'),
        (DISPLAY_COMMENT, '最热评论'),
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE,verbose_name="展示类型")
    content = models.CharField(max_length=500, blank=True, verbose_name="内容", help_text="如果设置的不是HTML类型，可为空")
    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time =  models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    @property
    def content_html(self):
        """直接渲染模板"""
        from main.models import Post
        from comment.models import Comment
        from django.template.loader import render_to_string


        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            context = {
                'posts': Post.latest_posts()
            }
            result = render_to_string('config/blocks/siderbar_posts.html', context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                'posts': Post.hot_post()
            }
            result = render_to_string('config/blocks/siderbar_posts.html', context)
        elif self.display_type == self.DISPLAY_COMMENT:
            context = {
                'comments': Comment.objects.filter(status=Comment.STATUS_NORMAL)        #此处为什么是用Comment类来调用？？
            }
            result = render_to_string('config/blocks/siderbar_comments.html', context)
        return result
