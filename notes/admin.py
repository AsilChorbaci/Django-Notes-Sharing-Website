from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from notes.models import Category, Note, Images

class NoteImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status' , 'image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status']


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status','image_tag')
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [NoteImageInline]
    prepopulated_fields = {'slug': ('title',)}

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'note']
    #readonly_fields = ('image_tag',)

admin.site.register(Category , CategoryAdmin)
admin.site.register(Note , NoteAdmin)
admin.site.register(Images)