# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('photogallery.views',
    (r'^$', 'list_galleries'),
    (r'^get_img/(?P<key>.+)/(?P<model>.+)/$', 'getpic2'),
    (r'^view-gallery/(?P<key>.+)$', 'show_gallery'),
    (r'^download/(?P<key>.+)/(?P<name>.+)$', 'download_file'),
)
