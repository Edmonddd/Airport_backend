from django.contrib import admin
from ImageModule.models import Imagefile


# Register your models here.
class ImagefileAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description', 'upload_date')
    
    '''filter options'''
    list_filter = ('description', )

    '''10 items per page'''
    list_per_page = 10
    
admin.site.register(Imagefile, ImagefileAdmin)