# -*- coding:utf-8 -*-
from django.shortcuts import render   #渲染器
from django.http import HttpResponseRedirect #路由重定向
from django.contrib.auth.decorators import user_passes_test, login_required #自带的验证登陆函数
from django.contrib.auth.models import User  #User和anth表
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #分页系统
from management.models import MyUser, Book, Img, word  #导入自定义model
from django.core.urlresolvers import reverse       #?url反向查询
from management.utils import permission_check      #导入自定义函数，验证用户权限
import models
from django_comments.models import Comment         # i m drunk

# Create your views here.

def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'management/index.html', content)  #render函数自动查找template目录下，template必须同manageapp同级


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/signup.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'management/login.html', content)


def logout(request):
    auth.logout(request)   #系统自带的登出函数
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'management/set_password.html', content)


@user_passes_test(permission_check)
def add_book(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_book = Book(
                name=request.POST.get('name', ''),
                author=request.POST.get('author', ''),
                category=request.POST.get('category', ''),
                price=request.POST.get('price', 0),
                publish_date=request.POST.get('publish_date', '')
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_book',
        'state': state,
    }
    return render(request, 'management/add_book.html', content)


def view_book_list(request):
    user = request.user if request.user.is_authenticated() else None
    category_list = Book.objects.values_list('category', flat=True).distinct()
    query_category = request.GET.get('category', 'all') #获取URL中参数category的值；如果请求里没有category，则给qu_c赋值all
    if (not query_category) or Book.objects.filter(category=query_category).count() is 0:
        query_category = 'all'
        book_list = Book.objects.all()
    else:
        book_list = Book.objects.filter(category=query_category)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        book_list = Book.objects.filter(name__contains=keyword)
        query_category = 'all'

    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_book',
        'category_list': category_list,
        'query_category': query_category,
        'book_list': book_list,
    }
    return render(request, 'management/view_book_list.html', content)


def detail(request):
    user = request.user if request.user.is_authenticated() else None
    book_id = request.GET.get('id', '')
    if book_id == '':
        return HttpResponseRedirect(reverse('view_book_list'))
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return HttpResponseRedirect(reverse('view_book_list'))
    content = {
        'user': user,
        'active_menu': 'view_book',
        'book': book,
    }
    return render(request, 'management/detail.html', content)


@user_passes_test(permission_check)  #装饰器，只有权限>1才能实现添加图片的功能
def add_img(request):
    user = request.user
    state = None
    if request.method == 'POST':
        try:
            new_img = Img(
                    name=request.POST.get('name', ''),
                    description=request.POST.get('description', ''),
                    img=request.FILES.get('img', ''),
                    book=Book.objects.get(pk=request.POST.get('book', ''))
            )
            new_img.save()
        except Book.DoesNotExist as e:
            state = 'error'
            print(e)
        else:
            state = 'success'
    content = {
        'user': user,
        'state': state,
        'book_list': Book.objects.all(),
        'active_menu': 'add_img',
    }
    return render(request, 'management/add_img.html', content)

def sub_comment(request): #实现对单词书的评论功能
    print request.POST
    book_id = request.POST.get('book_id')
    comment = request.POST.get('comment_content')
    new_comment = Comment.objects.create(
                content_type_id= 8,
                object_pk = int(book_id),
                site_id = 1,
                user = request.user,
                comment = comment,
       )
    new_comment.save()
    return HttpResponseRedirect('/view_book/detail?id=%s' % book_id)

def wordslist(request):
    try:
        user = request.user if request.user.is_authenticated() else None
        classs = request.GET.get('classs', '')
        n = request.POST.get('num')
        words = word.objects.filter(classs__contains = classs)[:n].exclude(flag = 1)
        content = {
         'user': user,
         'words': words,
        }
        return render(request, 'management/wordslist.html', content)
    except:
        #健壮性考虑，避免用户输入过大的单词数目
        return HttpResponseRedirect(reverse('numerror'))

def worddetail(request):
    user = request.user if request.user.is_authenticated() else None
    word_id = request.GET.get('id', '')
    if word_id == '':
        return HttpResponseRedirect(reverse('wordslist'))
    word1 = word.objects.get(pk=word_id)  #注意这里是pk!
    key = word1.kword                     #取出关键字
    swords = word.objects.filter(kword__contains = key).exclude(id = word_id)[:2]  #按照一个不合理需求，仅仅给出俩个近义词.
    content = {                                                                    #并且排除本单词本身
        'user': user,
        'word': word1,
        'swords':swords
    }
    return render(request, 'management/worddetail.html', content)


def sub_comment2(request): #单词详情页实现笔记功能
    print request.POST
    word_id = request.POST.get('word_id')
    comment = request.POST.get('comment_content')
    new_comment = Comment.objects.create(
                content_type_id= 13,  #这个id我真是醉了
                object_pk = int(word_id),
                site_id = 1,
                user = request.user,
                comment = comment,
       )
    new_comment.save()
    return HttpResponseRedirect('/worddetail/?id=%s' % word_id)

def setflag(request):  #标记这个单词我已经会背了
    user = request.user if request.user.is_authenticated() else None #数据库中就一张单词表，没有针对用户，所以这句话并没有什么意义
    word_id = request.POST.get('word_id')
    print word_id
    word.objects.filter(pk= word_id).update(flag = 1)
    return HttpResponseRedirect(reverse('wordslist'))

def nextone(request): #实现单词的详情页的翻页
    try:
        user = request.user if request.user.is_authenticated() else None
        word_id = request.POST.get('word_id')
        word_id = int(word_id) + 1   #int
        word1 = word.objects.get(pk=word_id)
        while (word1.flag):
            word_id = word_id + 1
            word1 = word.objects.get(pk=word_id)
        key = word1.kword    #取出关键字
        swords = word.objects.filter(kword__contains = key).exclude(id = word_id)[:2]  #按照一个不合理需求，仅仅给出俩个近义词.
        content = {
            'user': user,
            'word': word1,
            'swords':swords
        }
        return render(request, 'management/worddetail.html', content)
    except:  #健壮性考虑，背完了路由重定向至主页
        return HttpResponseRedirect(reverse('homepage'))

def numerror(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'user': user,
    }
    return render(request, 'management/numerror.html', content)

