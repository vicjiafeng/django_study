from django.contrib.syndication.views import Feed
from .models import Post

class AllPostsRssFeed(Feed):
    title="Django 博客"
    link = "/"           #跳转网址
    description = "Django 博客测试"
    def items(self):                      #显示内容条目
        return Post.objects.all()
    def item_title(self, item):            #显示内容条目的标题
        return '[%s] %s' % (item.category, item.title)
    def item_description(self, item):          #显示内容条目的描述
        return item.body
