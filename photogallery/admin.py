from django.contrib import admin
from photogallery.models import Gallery, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ['name', 'file']
    
class PhotoAdmin(admin.ModelAdmin):
    model = Photo

class GalleryAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)
    list_display = ('title', 'published', 'created')
    fieldsets = [
        (None,               {'fields': ['title', 'published']}),
        #('Data di pubblicazione', {'fields': ['pubblicare'], 'classes': ['collapse']}),
    ]


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Photo, PhotoAdmin)
