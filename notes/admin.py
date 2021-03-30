from django.contrib import admin

# Register your models here.
from notes.models import Category, Note

admin.site.register(Category)
admin.site.register(Note)