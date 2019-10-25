from django.shortcuts import render

from django.http import HttpResponse
from .models import Post,Tag, Category
from config.models import SideBar
# Create your views here.

def post_list(request, category_id=None, tag_id=None):      #从数据库中拿到所有的文章，然后显示title和摘要
    """content = 'post_list: category_id={category_id}, tag_id ={tag_id}'.format(              #{}与内容之间不能有空格
        category_id=category_id,
        tag_id=tag_id,
    )
    return HttpResponse(content)
    return render(request, 'main/list.html', context={'name':'post_list'})"""

    tag = None
    category = None

    if tag_id:
        """try:
            tag = Tag.objects.get(id=tag_id)    #tag与post是多对多的关系，所以需要先获取tag的对象 ？？
        except Tag.DoesNotExist:
            post_list = []
        else:      #try语句里也可以写else，表示没有意外，顺利执行的条件。可以
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)    #tag.post  再思考下--可能是多对多不允许吧。下次写的时候注意点"""
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        """post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Post.DoesNotExist:
                category = None
            else:
                post_list = post_list.filter(category_id=category_id)"""
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()           #显示最新的文章

    context = {
        'category':category,
        'tag':tag,
        'post_list':post_list,
        'sidebars': SideBar.get_all(),
    }

    context.update(Category.get_navs())         #??

    return render(request, 'main/list.html', context=context)




def post_detail(request, post_id):
    #return HttpResponse('detail')
    #return render(request, 'main/detail.html', context={'name':'post_detail'})
    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }

    context.update(Category.get_navs())

    return render(request, 'main/detail.html', context=context)