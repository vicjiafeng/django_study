import markdown
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm

# Create your views here.
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    #类视图paginate_by可以设定z分页功能，数字代表每页文章数目
    paginate_by = 2
    def get_queryset(self):
        return super(IndexView,self).get_queryset().order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     #父类生成传递给模版的字典
        paginator = context.get('paginator')             #字典用get方法
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        #自调用，显示分页导航数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)    #更新变量到context，返回字典
        return context
    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:          #没有分页，不需要导航条，返回空字典
            return {}
        left = []        #当前页左边连续页码号
        right = []        #当前页右边连续页码号
        left_has_more = False       #第一页后是否需要省略号
        right_has_more = False       #最后一页前是否需要省略号
        first = False                 #第一页页码
        last = False                  #最后一页页码
        page_number = page.number       #当前页码
        total_pages = paginator.num_pages       #总页码
        page_range = paginator.page_range        #分页页码列表
        if page_number == 1:
            right = page_range[page_number:page_number+2]    #获取左边连续2个页码
           #最右页码比总页码-1还小，则下面一行代码省略号需要，显示true
            if right[-1] < total_pages - 1:
                right_has_more = True
            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            if right[-1] < total_pages:
                last = True          #标记最后一页
        elif page_number == total_pages:      #请求的是最后一页的数据
            #获取左边连续页码号，这里只获取了当前页码后连续两个页码
            left = page_range[(page_number-3)if (page_number -3) > 0 else 0: page_number - 1]
            #左边页码比第二页还大
            if left[0] > 2:
                 # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号
                left_has_more = True
            if left[0] > 1:       #左边页码比第一页大，说明左侧连续页码不包含第一页页码
                first = True        #显示第一页页码
        else:   #用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号
            #获取左边连续两个页码[page_number-3:page_number-1]
            left = page_range[(page_number-3) if (page_number - 3) > 0 else 0:page_number - 1]
            #获取右边连续两个页码
            right = page_range[page_number:page_number+2]
            #是否需要显示最后一页/最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            ##是否需要显示第一页/第一页后的省略号
            if left[0] > 2:
                right_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
        }
        return data

'''
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,extensions=[
                                  'markdown.extensions.extra',
                                  'markdown.extensions.codehilite',
                                  'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
              }
    return render(request, 'blog/detail.html', context=context)
'''
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    def get(self,request,*args,**kwargs):
        response = super(PostDetailView,self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    def get_object(self,queryset=None):
        post = super(PostDetailView,self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                              ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post
    def get_context_data(self,**kwargs):
        context = super(PostDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({'form':form, 'comment_list':comment_list})
        return context

                    


class CategoryView(IndexView):
    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category).order_by('-created_time')
'''
def category(request,pk):
    category = get_object_or_404(Category, pk=pk)
    post_list=Post.objects.filter(category).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,          created_time__month=month).order_by('-created_time')
    return render(request,'blog/index.html', context={'post_list': post_list})
'''
class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self/kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(created_time__year=year, created_time__month = month)


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)
