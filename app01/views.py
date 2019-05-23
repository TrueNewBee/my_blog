from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from geetest import GeetestLib
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01 import forms
from bbs_demo import settings
from django.db.models import Count
from django.db.models import F
from bs4 import BeautifulSoup
import json
import os

"""
super_user: root zhen1996.....
user:  xiaohei   xiaohei1234
2018-9-28 21:26:56  完美的迭代啦!并且美化了页面
2018-9-29 18:41:47  优化了验证登入多写个接口而已  
2018-9-30 15:01:03  增加了 index页面显示所有文章, home显示用户所有的文章, 增加左侧页面显示文章分类
                    ,和日期归类(由于没有用MySQL,所以SQL语句用不了,显示不了!)
2018-10-1 16:43:54  增加了 点赞和踩灭的功能
2018-10-2 13:53:30  增加了评论和显示评论,子评论的功能, 并且在页面刷新的,直接通过Ajax添加<div>显示评论树
                    ps: 评论树就是在前端通过Ajax,动态的在父评论id下面添加子评论<div> 然后把内容填进去就好了
2018-10-3 14:03:22  增加了添加文件功能,并且增加了富文本编辑器这个插件!
                    基本上博客所有的功能全都实现完了!后面可以根据自己DIY优化
这是我昨晚一些迭代想法:
    1.获取用户信息得从cookies或session里面拿
    2.可以在顶部设置一个管理 跳转到个人文章管理页面
    3. 然后可以显示文章 就是图书馆管理系统的增删改查!
    4可以以后迭代一下!

2018-10-4 18:56:14   优化了个人博客页面的头顶样式 在个人博客页面又上角加了 添加文章的 a标签,,就这样实现了
                     只有登入用户才可以添加文章
下次迭代,做个管理文章的页面,类似于图书系统页面,然后仿照哪个来实现文章的增删改查就好了

2018-10-5 18:37:10   增加了一个文章管理的页面
2018-10-6 14:53:26   优化了各个文章显示时间,按时间最新开始排列,也就是定义个article_list =[]  pip
                     把文章放里面去,然后用了 reverse()方法,把里面文章倒叙排列,再传到前端显示就好了
                     
2019-1-30 17:21:20 在GitHub拿下源码,然后必须是Django1.11.1的才能打开,,我的现在电脑Django2.1的看看逻辑
把vue看完,然后用restframwork 做一个前后端分离的
                     
"""
# 2018-9-27 20:16:01
# def reg(request):
#     """先注册个用户"""
#     models.UserInfo.objects.create_user(username="alex", password="123")
#     return HttpResponse("o98k")

def music(request):
    return  render(request, "music.html")


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 使用极验滑动验证码的登录
def login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)
                ret["msg"] = "/index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    return render(request, "login_new.html")


# 处理极验 获取验证码的视图
def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 加了装饰器 可以不校验csrf
@csrf_exempt
def up(request):
    if request.method == "POST":
        file_obj = request.FILES.get("kouge")
        with open(file_obj.name, 'wb') as f:
            for line in file_obj:
                f.write(line)
        return HttpResponse("o98k")
    return render(request, "form_up.html")


# 2018-9-28 12:33:47
# 注册的视图函数
def register(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        print(request.POST)
        # 帮我做校验
        if form_obj.is_valid():
            # 校验通过，去数据库创建一个新的用户
            form_obj.cleaned_data.pop("re_password")
            avatar_img = request.FILES.get("avatar")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/index/"
            return JsonResponse(ret)
        else:
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            return JsonResponse(ret)
    # 生成一个form对象
    form_obj = forms.RegForm()
    return render(request, "register.html", {"form_obj": form_obj})


# 注销的视图函数
def logout(request):
    auth.logout(request)
    return redirect("/index/")


# 2018-9-29 18:38:59
# 校验用户名是否已被注册! 就是多写个接口
def check_username_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    print(username)
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已被注册！"
    return JsonResponse(ret)


# 显示index的视图函数
def index(request):
    # 定义一个文章列表
    article_list = []
    # 查询所有的文章列表
    articles = models.Article.objects.all()
    for i in articles:
        article_list.append(i)
    # 倒叙排列 实现时间最新
    article_list.reverse()
    return render(request, "index.html", {"article_list": article_list})


# 2018-9-30 15:01:10
# 个人博客主页
def home(request, username):
    # 定义一个文章列表
    article_list = []
    # 去UserInfo表里把用户对象取出来
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    # 如果用户存在需要将TA写的所有文章找出来
    blog = user.blog
    # 我的文章列表
    articles = models.Article.objects.filter(user=user)
    for i in articles:
        article_list.append(i)
    article_list.reverse()
    # 我的文章分类及每个分类下文章数
    # 将我的文章按照我的分类分组，并统计出每个分类下面的文章数
    # category_list = models.Category.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    # [{'title': '技术', 'c': 2}, {'title': '生活', 'c': 1}, {'title': 'LOL', 'c': 1}]
    # 统计当前站点下有哪一些标签，并且按标签统计出文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    # 按日期归档
    archive_list = models.Article.objects.filter(user=user).extra(
        select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
    ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")

    return render(request, "home.html", {
        "username": username,
        "blog": blog,
        "article_list": article_list,
    })


# 左侧菜单
def get_left_menu(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
    # 按日期归档  由于没有使用mysql数据库,故不能使mysql语句,所以不显示那个日期归档啦
    # archive_list = models.Article.objects.filter(user=user).extra(
    #     select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
    # ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")

    return category_list, tag_list


# 文章详情
def article_detail(request, username, pk):
    """
    :param request: 传入request参数
    :param username: 被访问的blog的用户名
    :param pk: 访问的文章的主键id值
    :return:
    """
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    blog = user.blog
    # 找到当前的文章
    article_obj = models.Article.objects.filter(pk=pk).first()
    # 所有评论列表
    comment_list = models.Comment.objects.filter(article_id=pk)
    return render(
        request,
        "article_detail.html",
        {
            "username": username,
            "article": article_obj,
            "blog": blog,
            "comment_list": comment_list,
        }
    )


# 2018-10-1 16:43:32
# 点赞或踩灭
def up_down(request):
    # 获取文章id
    article_id = request.POST.get('article_id')
    # 获取是点赞还是踩灭 就是True或False
    is_up = json.loads(request.POST.get('is_up'))
    # 获取user
    user = request.user
    response = {"state": True}
    try:
        # 把这条数据存到数据库
        models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)
        # 然后把点赞数+1  使用了F函数实现+1
        models.Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
    except Exception as e:
        # 第二次点击点赞或踩的按钮找到第一次数据,看是False还是True,返回到前端
        response["state"] = False
        response["fisrt_action"] = models.ArticleUpDown.objects.filter(user=user, article_id=article_id).first().is_up
    return JsonResponse(response)


# 2018-10-2 14:07:48
# 评论的视图
def comment(request):
    """ 就是找到pid . article_id, user_pk, content 然后去数据库创建内容"""
    pid = request.POST.get("pid")
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    user_pk = request.user.pk
    response = {}
    if not pid:     # 根评论
        comment_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk,content=content)
    else:
        comment_obj = models.Comment.objects.create(article_id=article_id, user_id=user_pk, content=content, parent_comment_id=pid)
    response["create_time"] = comment_obj.create_time.strftime("%Y-%m-%d")  # .strftime() 把时间对象转为字符串
    response["content"] = comment_obj.content
    response["username"] = comment_obj.user.username
    return JsonResponse(response)


# 评论树的视图
def comment_tree(request, article_id):
    # 从数据库查找父类评论对象  list强转,
    ret = list(models.Comment.objects.filter(article_id=article_id).values("pk", "content", "parent_comment_id"))
    return JsonResponse(ret, safe=False)


# 2018-10-3 13:49:37
# 添加文章的视图
def add_article(request):
    if request.method == "POST":
        title = request.POST.get('title')
        article_content = request.POST.get('article_content')
        user = request.user
        bs = BeautifulSoup(article_content, "html.parser")
        desc = bs.text[0:150]+"..."
        # 过滤非法标签
        for tag in bs.find_all():
            print(tag.name)
            if tag.name in ["script", "link"]:
                tag.decompose()
        article_obj = models.Article.objects.create(user=user, title=title, desc=desc)
        models.ArticleDetail.objects.create(content=str(bs), article=article_obj)
        return redirect("/blog/"+str(user)+"/")
    return render(request, "add_article.html")


# 编辑文章上传文件视图
def upload(request):
    obj = request.FILES.get("upload_img")
    path = os.path.join(settings.MEDIA_ROOT,"add_article_img",obj.name)
    with open(path, "wb") as f:
        for line in obj:
            f.write(line)
    ret = {
        "error": 0,
        "url": "/media/add_article_img/" + obj.name
    }
    return HttpResponse(json.dumps(ret))


# 2018-10-5 18:37:05
# 管理文章的url
def manage_article(request):
    # 定义一个articles_list列表
    article_list = []
    # 取出登入用户名字
    username = request.user.username
    user = models.UserInfo.objects.filter(username=username).first()
    # 如果用户存在需要将TA写的所有文章找出来
    blog = user.blog
    # 我的文章列表
    articles = models.Article.objects.filter(user=user)
    for i in articles:
        article_list.append(i)
    article_list.reverse()
    return render(request, "manage_article.html", {
        "username": username,
        "blog": blog,
        "article_list": article_list,
    })
