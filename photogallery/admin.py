from django.contrib import admin
from photogallery.models import Gallery, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ['imgname', 'file']
    list_display = ('imgname', 'admin_thumb', 'file')
    extra = 5
    
class PhotoAdmin(admin.ModelAdmin):
    model = Photo
    fields = ['gallery', 'imgname', 'file']
    list_display = ('admin_thumb','imgname')
    

class GalleryAdmin(admin.ModelAdmin):
    inlines = (PhotoInline,)
    list_display = ('title', 'published', 'created')
    list_filter = ('published',)
    search_fields = ('title',)
    fieldsets = [
        (None,               {'fields': ['title', 'description', 'published', 'imgname', 'file']}),
        #('Data di pubblicazione', {'fields': ['pubblicare'], 'classes': ['collapse']}),
    ]
    class Media:
        js = ("/assets/js/getfilename.js",)


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Photo, PhotoAdmin)