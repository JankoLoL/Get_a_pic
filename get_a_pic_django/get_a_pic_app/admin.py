from django.contrib import admin

from .models import *

admin.site.register(ThumbnailSize)
admin.site.register(UserProfile)
admin.site.register(Plan)
admin.site.register(Image)
admin.site.register(ExpiringLink)
