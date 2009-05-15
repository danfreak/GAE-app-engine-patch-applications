# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail

from google.appengine.ext import db
from mimetypes import guess_type
from photogallery.models import Gallery, Photo
from ragendja.dbutils import get_object_or_404, get_object, get_object_list
from ragendja.template import render_to_response


def list_galleries(request):
    return object_list(request, Gallery.all(), paginate_by=10)

def show_gallery(request, key):
    g = get_object(Gallery, key)

    images = None
    if g:
      images = get_object_list(Photo, "gallery =", g.key()).fetch(50)
    
    return render_to_response(request, 'gallery_detail.html', {'g': g, 'g_images': images})

def download_file(request, key, name):
    file = get_object_or_404(Gallery, key)
    if file.imgname != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.file,
        content_type=guess_type(file.imgname)[0] or 'application/octet-stream')

def view_img(request, key, name):
    file = get_object_or_404(Photo, key)
    if file.imgname != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.file,
        content_type=guess_type(file.imgname)[0] or 'application/octet-stream')
        
def getpic2(request, key, model):
    #print model
    file = get_object_or_404(Gallery, key)
    
    return HttpResponse(file.file,
        content_type=guess_type(file.imgname)[0] or 'application/octet-stream')

def thumbnailer(request, key, name):
    file = get_object_or_404(Photo, key)
    if file.imgname != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.thumb_s,
        content_type=guess_type(file.imgname)[0] or 'application/octet-stream')