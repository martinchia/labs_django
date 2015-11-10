# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:39:57 2015

@author: martin
"""
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from books.models import Author,book
from django.core.exceptions import ObjectDoesNotExist
import re



def home(request):
    disk={"contain":''}
    if request.POST:    
        try:
            if request.POST['check']=='author':
                disk['auth']=True
                answer=Author.objects.get(Name=request.POST['textfield'])
                disk["item_list"]=[answer.Name,answer.Age,answer.Country]
                author_book=book.objects.filter(AuthorID=answer)
                disk["a_list"]=[[item.ISBN,item.Title,item.Publisher,\
                item.PublishDate,item.Price] for item in author_book]
            elif request.POST['check']=='book':
                disk['book']=True
                answer=book.objects.filter(Title=request.POST['textfield']) 
                disk["a_list"]=[[item.ISBN,item.Title,item.Publisher,\
                item.PublishDate,item.Price,item.AuthorID.Name,\
                item.AuthorID.Age,item.AuthorID.Country]for item in answer]
        except ObjectDoesNotExist:
            disk["contain"]='ObjectDoesNotExist'
        except:
            disk["contain"]='你还没有选择查询方式'
    homepage=render_to_response('html/home.html',disk,\
    context_instance=RequestContext(request))
    return HttpResponse(homepage)
    
    
def checkbook(request):
    isbn=re.findall("(?<=\/checkbook\/)\d*",request.path)[0]  
    disk={}
    abook=book.objects.get(ISBN=isbn)
    alist=[abook.ISBN,abook.Title,abook.Publisher,abook.PublishDate,\
    abook.Price,abook.AuthorID.Name,abook.AuthorID.Age,abook.AuthorID.Country]
    disk={'a_list':alist}
    page=render_to_response('html/checkbook.html',disk,\
    context_instance=RequestContext(request))
    return HttpResponse(page)
    
def delete(request):
    item=re.findall("(?<=\/delete\/)\d*",request.path)[0]
    book.objects.get(ISBN=item).delete()
    return home(request)
    
def books(request):    
    disk={"exist":False,'isbn':''}   
    if request.path!="/book/":
        isbn=re.findall("(?<=\/book\/)\d*",request.path)[0]
        abook=book.objects.get(ISBN=isbn)
        list_=[abook.ISBN,abook.Title,abook.AuthorID.Name,abook.Publisher\
        ,str(abook.PublishDate.year)+'-'+str(abook.PublishDate.month)+'-'+\
        str(abook.PublishDate.day),abook.Price]
        disk={"exist":False,'isbn':'','list':list_}
        if request.POST:
            name=request.POST['AuthorName']
            if request.POST['ISBN']=='' or\
                    request.POST['Title']=='' or \
                    request.POST['Publisher']=='' or\
                    request.POST['Price']=='':
                        disk={"exist":False,'isbn':'有缺省项'}
            elif not re.match('\d{13}$',request.POST['ISBN']):
                disk={"exist":False,'isbn':'isbn不符合格式，要求13位数字!'}
            else:                
                try:
                    if request.POST["ISBN"]!=abook.ISBN:
                        book.objects.get(ISBN=request.POST["ISBN"])
                        disk['isbn']='ISBN冲突'
                    else:
                        raise ObjectDoesNotExist
                except ObjectDoesNotExist:
                    try:
                        anauth=Author.objects.get(Name=name)
                        abook.ISBN=request.POST['ISBN']
                        abook.save()
                        abook.Title=request.POST['Title']
                        abook.save()
                        abook.Publisher=request.POST['Publisher']
                        abook.save()
                        abook.PublishDate=request.POST['year']+'-'+\
                                 request.POST['month']+'-'+\
                                 request.POST['day']
                        abook.save()
                        abook.AuthorID=anauth
                        abook.save()
                        book.objects.get(ISBN=isbn).delete()
                        disk={"exist":False,'isbn':'修改成功！'}
                    except ObjectDoesNotExist:
                        disk["exist"]=True
                        disk['isbn']='作者不存在或书籍已经存在'                                                    
    else:
        if request.POST:
            name=request.POST['AuthorName']
            if request.POST['ISBN']=='' or\
                    request.POST['Title']=='' or \
                    request.POST['Publisher']=='' or\
                    request.POST['Price']=='':
                        disk={"exist":False,'isbn':'有缺省项'}
            elif not re.match('\d{13}$',request.POST['ISBN']):
                disk={"exist":False,'isbn':'isbn不符合格式，要求13位数字!'}
            else:
                try:
                    anauth=Author.objects.get(Name=name)
                    new=book(ISBN=request.POST['ISBN'],
                             Title=request.POST['Title'],
                             Publisher=request.POST['Publisher'],
                             PublishDate=request.POST['date'],
                             Price=request.POST['Price'],
                             AuthorID=anauth   )                        
                    new.save()
                    disk={"exist":False,'isbn':'添加成功！'}
                except ObjectDoesNotExist:
                    disk["exist"]=True
                    disk['isbn']='作者不存在或书籍已经存在'
    page=render_to_response('html/book.html',disk,context_instance=\
    RequestContext(request))

    return HttpResponse(page)
    
    
def author(request):
    disk={'text':''}
    if request.POST:
        if not request.POST['Name'] or request.POST['Age']\
        or request.POST['Country']:
            disk['text']='有缺省项！'
        else:
            new=Author(Name=request.POST['Name'],\
                       Age=request.POST['Age'],\
                       Country=request.POST['Country'],
                        )
            new.save()
            disk['text']='添加成功！'
    page=render_to_response('html/author.html',disk, context_instance=\
    RequestContext(request))
    return HttpResponse(page)