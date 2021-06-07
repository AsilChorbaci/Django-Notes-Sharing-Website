from django.contrib import admin
from home.models import Setting, ContactFormMessage, FAQ


# Register your models here.

class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at' ,'status']

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject','message','phone','status']
    list_filter = ['status']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['notenumber', 'question', 'answer',  'status']
    list_filter = ['status']

admin.site.register(FAQ, FAQAdmin)
admin.site.register(Setting , SettingAdmin)
admin.site.register(ContactFormMessage,ContactFormMessageAdmin)