from django.contrib import admin
from myblog.models import File, Categoria, News, Page
from myblog.forms import FileForm


class FileInline(admin.TabularInline):
    model = File
    fields = ['file']
    #used to set filename automagically
    form = FileForm
    extra = 5
    
class FileAdmin(admin.ModelAdmin):
    model = File
    list_display = ('thumb','name')

class NewsAdmin(admin.ModelAdmin):
    inlines = (FileInline,)
    list_display = ('title', 'category', 'published', 'created')
    search_fields = ('title',)
    list_filter = ('published',)
    fieldsets = [
        (None,               {'fields': ['category', 'title', 'content', 'published']}),
        ('Data di pubblicazione', {'fields': ['pubblicare'], 'classes': ['collapse']}),
    ]

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')
    fields = ['name']
    
class PageAdmin(admin.ModelAdmin):
    inlines = (FileInline,)
    list_display = ('title', 'subpage_of', 'published', 'created')
    search_fields = ('title',)
    list_filter = ('published',)
    fields = ['subpage_of', 'title', 'slug', 'content', 'published']

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(News, NewsAdmin)
