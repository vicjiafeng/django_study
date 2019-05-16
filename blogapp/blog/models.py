import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100)

class Tag(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    
    def save(self, *args, **kwargs):             #定义‘摘要’的方法
        if not self.excerpt:
            #实例 Markdown类， 渲染body文本
            md = markdown.Markdown(extensions=[
                                   'markdown.extensions.extra',
                                   'markdown.extensions.codehilite',
                                   ])
            #渲染文本成html，然后去掉tags，b摘取前54个字符给excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        #super调用父类post 保存数据到数据库
        super(Post, self).save(*args, **kwargs)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #新增views字段记录阅读量
    views = models.PositiveIntegerField(default=0, editable=False)
    #image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)

    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})
    class Meta:
        ordering = ['created_time']
