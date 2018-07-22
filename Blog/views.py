import json
import redis

from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from .models import ArticleColumn, ArticlePost

# Create your views here.

@login_required(login_url="/auth/login")
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        column = ArticleColumn.objects.filter(user = request.user)
        return render(request, "article/column/article_column.html", {"column": column})

    if request.method == "POST":
        data = request.POST
        print(data)
        name = data.get("column_name", '')
        print(name)

        error = {"msg": "error", "status": False, "state":403}
        if name == '':
            return HttpResponse("1")#不可以空
        column = ArticleColumn.objects.filter(user = request.user, column=name)
        if column:
           return HttpResponse("2")#已经存在
           
        ArticleColumn.objects.create(user = request.user, column=name)
        return HttpResponse("0") #ok


@login_required(login_url="/auth/login")
@csrf_exempt
def exit_column(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        old_id = data.get("old_id", '')
        new_name = data.get("new_name", '')

        column_exit = ArticleColumn.objects.filter(id=old_id, user=request.user)
        if column_exit:
            column = column_exit[0]
        else:
            return HttpResponse("2") #要修改的列不存在

        if new_name == '':
            return HttpResponse("1") #新列名为空

        column.column = new_name    
        return HttpResponse("0") #创建成功


@login_required(login_url="/auth/login")
@csrf_exempt
def add_post(request):
    user = request.user
    if request.method == "GET":
        column = ArticleColumn.objects.filter(user = user)
        return render(request, "article/post.html",{"columns":column})

    if request.method == "POST":
        data = request.POST
        title = data.get("title", '')
        article = data.get("article", '')
        chose = data.get('chose', '')
        if chose == "":
            return HttpResponse("没有选择列")

        column = ArticleColumn.objects.filter(column=chose,user=user)[0]

        post = ArticlePost()
        post.column = column
        post.author = user
        post.body = article
        post.title = title
        post.save()
        print(post)
        return HttpResponse("创建成功")


def article_list(request):
    articles = ArticlePost.objects.filter(author=request.user)
    return render(request, "article/article_list.html", {"articles": articles})

# def show_article(request, pid, slug):
#     article = ArticlePost.objects.filter(id=pid, slug=slug)[0]
#     return render(request, "article/show_article.html", {"article": article})

#记录文章浏览次数
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def article_detail(request, pid, slug):
    article = ArticlePost.objects.filter(id=pid, slug=slug)
    if article:
        article = article[0]
        total_views = r.incr("articel:{}:views".format(article.id)) 
        r.zincrby("article_ranking", article.id, 1)

        article_ranking = r.zrange("article_ranking", 0, -1, desc=True)[:10]
        article_ranking_ids = [int(id) for id in article_ranking]
        most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
        most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
        print(most_viewed)
        return render(request, "article/show_article.html", {"atricle": article, "total_views": total_views, "most_viewed":most_viewed})
    else:
        return HttpResponse("抱歉,没有找到文章")    


