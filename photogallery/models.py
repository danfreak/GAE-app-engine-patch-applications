# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

from django.template.defaultfilters import slugify

from mycommon.image_kit import flickr_thumb, resize_to_max, resize_to

class Gallery(db.Model):
    #Basic user profile with personal details
    title = db.StringProperty(required=True)
    description = db.TextProperty("Description")
    published = db.BooleanProperty("Pubblicato")
    created = db.DateTimeProperty("Created", auto_now_add = True)
    updated = db.DateTimeProperty("Updated", auto_now = True)
    imgname = db.StringProperty("Nome immagine")
    file = db.BlobProperty("Immagine", required=True)
    
    class Meta:
       verbose_name_plural = "galleries"
       ordering = ('-created')
       
    
    def __unicode__(self):
        return '%s' % (self.title)

    @permalink
    def get_absolute_url(self):
        return ('photogallery.views.show_gallery', (), {'key': self.key()})
    
    def put(self):
      thumb = db.Blob(resize_to(self.file, 222, 152))
      
      self.file  = thumb
      #self.imgname = 'gallery.jpg'
      
      key = super(Gallery, self).put()
      # do something after save
      return key
    
    save = put

signals.pre_delete.connect(cleanup_relations, sender=Gallery)


class Photo(db.Model):
    gallery = db.ReferenceProperty(Gallery, required=False, collection_name='gallery_set')
    imgname = db.StringProperty()
    file = db.BlobProperty(required=True)
    thumb_m = db.BlobProperty()
    thumb_s = db.BlobProperty()
    created = db.DateTimeProperty("Created", auto_now_add = True)
    updated = db.DateTimeProperty("Updated", auto_now = True)
    
    class Meta:
       ordering = ('-created',)
       
    def put(self):
      #resize file to fit max dimensions
      self.file  = resize_to_max(self.file, 600, 600)
      #create thumbs
      t_s = db.Blob(flickr_thumb(self.file, 100))
      t_m = db.Blob(flickr_thumb(self.file, 200))
      #print t_s
      self.thumb_s  = t_s
      self.thumb_m  = t_m
      
      key = super(Photo, self).put()
      # do something after save
      return key
    
    save = put
    
    def admin_thumb(self):
    	return """<a href="/admin/photogallery/photo/%s/"><img src="/gallery/thumb_m/%s/%s" alt="tiny thumbnail image" /></a>"""%(self.key(), self.key(), self.imgname)
    #admin_thumb.short_description = _('Thumbnail')
    admin_thumb.allow_tags = True

    @permalink
    def get_absolute_url(self):
        return ('photogallery.views.view_img', (), {'key': self.key(),
                                                    'name': self.imgname})
   
    def __unicode__(self):
        return u'%s' % self.imgname