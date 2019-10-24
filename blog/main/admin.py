from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html

from django.contrib.auth import get_permission_codename    #用来重写get_premission，来确定用户有没有相关权限

from blog.custom_site import custom_site
from .models import Post, Category, Tag
from .adminForms import PostAdminForm

# Register your models here.

PERMISSION_API = "http://permission.sso.com/has_perm?user={}&perm_code={}"    #在需要的类下重写方法


"""
这个类用来增加功能，使得分类页面可以对文章进行编辑
"""
class PostInline(admin.TabularInline):         #还有个样式是StackedInline,用来CategoryAdmin这个类里

    fields = ('title','desc')
    extra = 1   #控制额外多几个
    model = Post



@admin.register(Category, site=custom_site)    #注册绑定,装饰器模式
class CategoryAdmin(admin.ModelAdmin):

    inlines = [PostInline]         # 对应上面的PostInline类，没什么用，因为上面类里只定义的两个字段，无法添加完整文章

    list_display = ('name','status','is_nav','created_time','post_count')   #显示用
    fields = ('name','status','is_nav','owner')                #添加时出现

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self,obj):
        return obj.post_set.count()           #obj.post_set 当前文章集合，django自带，应该是

    post_count.short_description = '文章数量'

@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)





class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只显示当前用户分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'          #查询时用的URL参数的名字

    def lookups(self, request, model_admin):       #返回要展示的内容，和查询用的id
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):        #根据URL QuerySet的内容返回列表页数据
        category_id = self.value()      #self.value() = owner_category的值
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset




@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):

    form = PostAdminForm       #上面form导入一下，下面这儿写一下，就应用成功了adminForms.py这个里的form组建，而不是原来的ModelAdmin

    list_display = [
        'title','category','status',
        'created_time','operator'       #有新加的字段operator
    ]
    list_display_links = []             #用来配置哪些字段可以作为链接。可配置为NONE

    #list_filter = ['category', ]        用来配置页面过滤器
    list_filter = [CategoryOwnerFilter]   #重写好的filter在这儿配置
    search_fields = ['title','category_name']   #配置搜索字段

    actions_on_top = True      #是否显示置顶
    actions_on_bottom = True


    #编辑页面
    save_on_top = True         #保存，编辑，及编辑并新建按钮是否保存在顶部

    exclude = ('owner',)       #填写字段的时候，该字段不用重写，默认为当前登陆用户

    """fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )"""

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title','category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息',{
            'classes': ('collapse',),
            'fields':('tag',),
        })
    )

    filter_horizontal = ('tag',)    #django用来显示多对多字段，横排或者竖排


    def operator(self, obj):    #自定义函数，参数是固定的，就是当前行对象，可以返回html
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:main_post_change', args=(obj.id,))          #此处的blog_post_change可能会有问题，也是django的定义方法
                                                                           #此处admin改过，为了适应新的site站点
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):          #用来约束用户只能看到自己写的文章，重写get_queryset方法
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


    def has_add_permission(self, request):           #用来重写用户对该表的权限
        opts = self.opts
        codename = get_permission_codename('add', opts)
        perm_code = "%s.%s" % (opts.app_label, codename)
        resp = request.get(PERMISSION_API.format(request.user.username, perm_code))
        if resp.status_code == 200:
            return True
        else:
            return False


    class Media:     #用来在django的admin的页面中添加bootstrap的css效果, 兼容性不好，需要调整，有空查，问题保留
        css = {
            'all' : ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js", )





