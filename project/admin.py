from django.contrib import admin
from .models import *


@admin.register(Project)
class ProjectModelAdmin(admin.ModelAdmin):
    pass


@admin.register(File)
class FileModelAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(Folder)
class FolderModelAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(ShareLink)
class ShareLinkModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'project')


@admin.register(Member)
class MemberModelAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role')
