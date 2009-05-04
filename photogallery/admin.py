from django.contrib import admin
from photogallery.models import Gallery, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ['name', 'file']
    
class PhotoAdmin(admin.ModelAdmin):
    model = Photo
    fields = ['gallery', 'name', 'file']
    list_display = ('thumb','name')


class GalleryAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)
    list_display = ('title', 'published', 'created')
    list_filter = ('published',)
    search_fields = ('title',)
    fieldsets = [
        (None,               {'fields': ['title', 'published', 'image']}),
        #('Data di pubblicazione', {'fields': ['pubblicare'], 'classes': ['collapse']}),
    ]


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Photo, PhotoAdmin)