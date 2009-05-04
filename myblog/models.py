# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations
from django.template.defaultfilters import slugify
from google.appengine.ext.db import polymodel

from mycommon.image_kit import flickr_thumb

class Categoria(db.Model):
    name = db.StringProperty("Name", required = True)
    created = db.DateTimeProperty("Created", auto_now_add = True)
    updated = db.DateTimeProperty("Updated", auto_now = True)
    
    def __str__(self):
        return str(self.name)
    def __unicode__(self):
        return '%s' % (self.name)
    class Meta:
       verbose_name_plural = "categoria"


class News(db.Model):
    category = db.ReferenceProperty(Categoria, collection_name = "categoria")
    title = db.StringProperty("Title", required = True)
    content = db.TextProperty("Content", required = True)
    slug = db.StringProperty("Slug")
    published = db.BooleanProperty("Pubblicato")
    pubblicare = db.DateTimeProperty("Pubblicare il")
    created = db.DateTimeProperty("Created", auto_now_add = True)
    updated = db.DateTimeProperty("Updated", auto_now = True)
    
    class Meta:
       verbose_name_plural = "news"
    def __str__(self):
        return str(self.title)
        
    def __unicode__(self):
        return '%s' % (self.title)


class Page(db.Model):
    subpage_of = db.SelfReferenceProperty("Sottopagina di")
    title = db.StringProperty("Title", required = True)
    slug = db.StringProperty("Slug")
    content = db.TextProperty("Content", required = True)
    menu_title= db.StringProperty("Menu title")
    published = db.BooleanProperty("Pubblicato")
    created = db.DateTimeProperty("Created", auto_now_add = True)
    updated = db.DateTimeProperty("Updated", auto_now = True)
    
    def get_url(self):
        return "/%s" % self.slug

    def __str__(self):
        return str(self.title)
        
    def __unicode__(self):
        return '%s' % (self.title)
        
    def put(self):
      #self.slug = slugify(self.title)
      
      key = super(Page, self).put()
      # do something after save
      return key
    
    save = put
    


class File(db.Model):
    #owner = db.ReferenceProperty(Person, required=False, collection_name='file_set')
    page = db.ReferenceProperty(Page, required=False, collection_name='file_set')
    news = db.ReferenceProperty(News, required=False, collection_name='file_set')
    #gallery = db.ReferenceProperty(Gallery, required=True, collection_name='file_set')
    name = db.StringProperty()
    file = db.BlobProperty(required=True)
    thumb_m = db.BlobProperty()
    thumb_s = db.BlobProperty()
    
    def put(self):
      t_s = db.Blob(flickr_thumb(self.file, 100))
      t_m = db.Blob(flickr_thumb(self.file, 200))
      #print t_s
      self.thumb_s  = t_s
      self.thumb_m  = t_m
      
      key = super(File, self).put()
      # do something after save
      return key
    
    save = put
    
    def thumb(self):
    	return """<a href="/admin/myblog/file/%s/"><img src="/get_img/%s/" alt="tiny thumbnail image" /></a>"""%(self.key(), self.key())
    thumb.allow_tags = True
    
    @permalink
    def get_absolute_url(self):
        return ('myblog.views.download_file', (), {'key': self.key(),
                                                  'name': self.name})
    def __unicode__(self):
        return u'File: %s' % self.name