from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    把其他admin里的get_query(列表只展示当前用户的)和save_model(默认owner为当前登陆用户),这两个方法抽取出来
    """

    exclude = ('owner', )

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner = request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return  super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

