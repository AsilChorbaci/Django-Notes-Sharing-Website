from django.contrib import admin
from home.models import Setting, ContactFormMessage
# Register your models here.

class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at' ,'status']

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject','message','phone','status']
    list_filter = ['status']

admin.site.register(Setting , SettingAdmin)
admin.site.register(ContactFormMessage,ContactFormMessageAdmin)