from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):     #分类
    STATUS_NORMAL = 1
    STATUS_DELETE= 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    @classmethod
    def get_navs(cls):        #分类到导航界面
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = [] #categories.filter(is_nav=True)
        normal_categories = [] #categories.filter(is_nav=False)

        for cate in categories:        #通过判断来减少ategories.filter(is_nav=False)对数据库的查询，业务大的时候，尽量减少查询数据库
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }

class Tag(models.Model):         #标签
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Post(models.Model):         #文章
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
        (STATUS_DRAFT, "草稿"),
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="正文必须是MarkDown格式")  #??
    category = models.ForeignKey(Category, verbose_name="分类")   #分类可以修改为一个集合,或许
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS, verbose_name="状态")

    pv = models.PositiveIntegerField(default=1)    #用来记录点击率
    uv = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']   #根据id降序排列

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id = tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')   #用来解决前端页面上post.category.name,
                                                                                                            #post.owner.user等外健来查询的时候，每次查一条的问题
        return post_list,tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id = category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')
        return post_list, category

    @classmethod          #@classmethod 和 @staticmethod一样，不需要实例化就可以直接用类名进行调用。一个是静态方法，一个是类方法
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    @classmethod
    def hot_post(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

