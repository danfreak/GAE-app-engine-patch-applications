# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('myblog.views',
    (r'^create_admin_user$', 'create_admin_user'),
    (r'^$', 'home'),
    (r'^news/$', 'list_news'),
    (r'^news/(?P<key>.+)$', 'view_news'),
    (r'^get_img/(?P<key>.+)/$', 'getpic2'),
    (r'^download/(?P<key>.+)/(?P<name>.+)$', 'download_file'),
    (r'^content/(?P<slug>.+)/$', 'view_page'),
)
