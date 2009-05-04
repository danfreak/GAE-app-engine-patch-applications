# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations
from django.template.defaultfilters import slugify

from mycommon.image_kit import flickr_thumb

class Gallery(db.Model):
    #Basic user profile with personal details
    title = db.StringProperty(required=True)
    description = db.TextProperty("Description")
    published = db.BooleanProperty("Pubblicato")
    created = db.DateTimeProperty("Created", auto_now_add = True)
    updated = db.DateTimeProperty("Updated", auto_now = True)
    
    class Meta:
       verbose_name_plural = "galleries"
    
    def __unicode__(self):
        return '%s' % (self.title)

    @permalink
    def get_absolute_url(self):
        return ('gallery.views.show_gallery', (), {'key': self.key()})

signals.pre_delete.connect(cleanup_relations, sender=Gallery)


class Photo(db.Model):
    gallery = db.ReferenceProperty(Gallery, required=False, collection_name='gallery_set')
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
      
      key = super(Photo, self).put()
      # do something after save
      return key
    
    save = put
    
    def thumb(self):
    	return """<a href="/admin/myblog/file/%s/"><img src="/get_img/%s/" alt="tiny thumbnail image" /></a>"""%(self.key(), self.key())
    thumb.allow_tags = True

    @permalink
    def get_absolute_url(self):
        return ('gallery.views.download_file', (), {'key': self.key(),
                                                  'name': self.name})

    def __unicode__(self):
        return u'%s' % self.name