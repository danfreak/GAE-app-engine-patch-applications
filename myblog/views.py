# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail

from google.appengine.ext import db
from mimetypes import guess_type

from myblog.models import News, Page, File, Categoria
from photogallery.models import Gallery, Photo
from ragendja.dbutils import get_object_or_404, get_object, get_object_list
from ragendja.template import render_to_response

def home(request):
    return object_list(request, News.all(), paginate_by=5)
    
def list_news(request, category):
    category = db.Query(Categoria).filter("name =", category).get()
    if category:
      return object_list(request, News.all().order('-created').filter('published =', True).filter('category  =', category.key()), paginate_by=5)
    else:
      return render_to_response(request, 'no_items.html')

def list_mostre(request):
    category = db.Query(Categoria).filter("name =", 'mostre').get()
    if category:
      return object_list(request, News.all().order('-created').filter('published =', True).filter('category  =', category.key()), paginate_by=5)
    else:
      return render_to_response(request, 'no_items.html')

def view_news(request, key):
    p = db.Query(News).filter("slug =", key).get()
    images = None
    if p:
      images = db.Query(File).filter("news =", p.key()).fetch(20)
    #print p.title
    return render_to_response(request, 'news_detail.html', {'news': p, 'p_images': images})
    
def view_page(request, slug):
    p = db.Query(Page).filter("slug =", slug).get()
    images = None
    if p:
      images = db.Query(File).filter("page =", p.key()).fetch(20)
    
    return render_to_response(request, 'page_detail.html', {'page': p, 'current': request, 'p_images': images})
    #return object_detail(request, Page.all(), slug)
    
def get_last_galleries():
  
  gall = Gallery.all()
  gall.filter("published = ", True)
  gall.order('-created')
  """
  for g in gall:
    if n%3:
      n=+
    newgall[]
  """
  return gall
    
def download_file(request, key, name):
    file = get_object_or_404(File, key)
    if file.name != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.file,
        content_type=guess_type(file.name)[0] or 'application/octet-stream')


def getpic2(request, key, type = 'thumb_s'):
    file = get_object_or_404(File, key)
    return HttpResponse(file.type,
        content_type=guess_type(file.name)[0] or 'application/octet-stream')
    
def get_right_pic(request, key, name):
    file = get_object_or_404(File, key)
    if file.name != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.thumb_w,
        content_type=guess_type(file.name)[0] or 'application/octet-stream')

def thumbnailer(request, key, name):
    file = get_object_or_404(File, key)
    if file.name != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.thumb_s,
        content_type=guess_type(file.name)[0] or 'application/octet-stream')
                
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
