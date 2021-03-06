# -*- coding: utf-8 -*-
import logging
from django.contrib import admin
from .forms import ImageForm
from .models import Album, Gallery, Image


logger = logging.getLogger(__name__)


class ImageInline(admin.TabularInline):
    model = Image


class GalleryAdmin(admin.ModelAdmin):
    """
    Admin class for the gallery model.
    """
    list_display = ['user','name', 'path', 'modified']
    inlines = [ImageInline]


class ImageAdmin(admin.ModelAdmin):
    """
    Admin class for the image model.
    """
    form = ImageForm
    list_display = ['gallery', 'name', 'path', 'modified']


class AlbumAdmin(admin.ModelAdmin):
    """
    Admin class for the image model.
    """
    list_display = ['gallery', 'name','modified']


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Album)

