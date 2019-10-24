from django.contrib.admin import AdminSite

"""
这个类用来一个站点对应多个site
通过继承AdminSite类来自定义自己的site，
实现用户管理模块和文章分类等数据的管理模块分开


实现的时候，还需要修改所有app下的admin里的register，即model通过装饰模式注册那一部分
以及涉及到站点的函数，例如reverse部分，都需要修改
最后需要修改url.py文件
"""

class CustomSite(AdminSite):
    site_header = 'blog'
    site_title = 'blog管理后台'
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')