from django.contrib import admin
from samklang_media.models import Document#, Image

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'user', 'group', 'submit_date')
    list_filter = ('submit_date', 'group', 'user')

admin.site.register(Document, DocumentAdmin)
