# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail

from google.appengine.ext import db
from mimetypes import guess_type

from myblog.models import News, Page, File
from photogallery.models import Gallery, Photo
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response

def home(request):
    return object_list(request, News.all(), paginate_by=2)
    
def list_news(request):
    return object_list(request, News.all(), paginate_by=2)

def view_news(request, slug):
    return object_detail(request, News.all(), slug)
    
def view_page(request, slug):
    p = db.Query(Page).filter("slug =", slug).get()
    gall = Gallery.all()
    gall.filter("published = ", True)
    gall.order('-created')
    #print p.title
    return render_to_response(request, 'page_detail.html', {'page': p, 'galleries': gall})
    #return object_detail(request, Page.all(), slug)
    
def download_file(request, key, name):
    file = get_object_or_404(File, key)
    if file.name != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.file,
        content_type=guess_type(file.name)[0] or 'application/octet-stream')

def getpic2(request, key):
    file = get_object_or_404(File, key)
    
    return HttpResponse(file.thumb_s,
        content_type=guess_type(file.name)[0] or 'application/octet-stream')
    
"""
from google.appengine.api import images

def getpic2(request, key, w=100, h=100):
    pic = get_object_or_404(File, key)
    if pic == None:
        raise Http404('Could not find file!')
    
    raw_img = images.Image(pic.file)
    if w!="" and h!="":
        raw_img.resize(width=int(w), height=int(h))
    
    raw_img.im_feeling_lucky()
    thumbnail = raw_img.execute_transforms(output_encoding=images.JPEG)

    return HttpResponse(thumbnail, content_type=guess_type(pic.name)[0] or 'application/octet-stream')
"""

def create_admin_user(request):
    user = User.get_by_key_name('admin')
    if not user or user.username != 'admin' or not (user.is_active and
            user.is_staff and user.is_superuser and
            user.check_password('admin')):
        user = User(key_name='admin', username='admin',
            email='admin@localhost', first_name='Boss', last_name='Admin',
            is_active=True, is_staff=True, is_superuser=True)
        user.set_password('admin')
        user.put()
    return render_to_response(request, 'myblog/admin_created.html')
