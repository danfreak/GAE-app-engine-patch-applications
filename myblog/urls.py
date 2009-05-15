# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('myblog.views',
    (r'^create_admin_user$', 'create_admin_user'),
    (r'^$', 'view_page', {'slug' : 'home'}),
    (r'^news/$', 'list_news', {'category' : 'news'}),
    (r'^mostre-arte-padova/$', 'list_news', {'category' : 'mostre'}),
    (r'^news/(?P<key>.+)$', 'view_news'),
    (r'^get_img/(?P<key>.+)/$', 'getpic2'),
    (r'^thumb_w/(?P<key>.+)/(?P<name>.+)$', 'get_right_pic'),
    (r'^download/(?P<key>.+)/(?P<name>.+)$', 'download_file'),
    (r'^thumb/(?P<key>.+)/(?P<name>.+)$', 'thumbnailer'),
    (r'^(?P<slug>.+)/$', 'view_page'),
)
