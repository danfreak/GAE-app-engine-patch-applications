# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail

from google.appengine.ext import db
from mimetypes import guess_type
from photogallery.models import Gallery, Photo
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response

def list_galleries(request):
    return object_list(request, Gallery.all(), paginate_by=10)

def show_gallery(request, key):
    return object_detail(request, Gallery.all(), key)

def download_file(request, key, name):
    file = get_object_or_404(File, key)
    if file.name != name:
        raise Http404('Could not find file with this name!')
    return HttpResponse(file.file,
        content_type=guess_type(file.name)[0] or 'application/octet-stream')
