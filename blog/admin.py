from django.contrib import admin
from . models import Blog, Category, Tag
from core.models import Report
from core.resource import ReportResource
from import_export.admin import ImportExportModelAdmin

@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin):
    list_display = ('title','isActive','showIndex','updated','created')
    prepopulated_fields= {'slug':('title',)}
    search_fields = ('title','description')
    list_filter = ('isActive','showIndex')

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    prepopulated_fields= {'slug':('name',)}
    search_fields = ('name',)
@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    prepopulated_fields= {'slug':('name',)}
    search_fields = ('name',)