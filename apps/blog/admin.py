from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from tinymce.widgets import TinyMCE
from django import forms
from adminsortable2.admin import SortableAdminMixin

from .models import Blog, Category, Tag, Menu


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Menu)
class MenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'seat_number', 'category', 'link')


class BlogForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Blog
        fields = "__all__"


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    list_display = ["title", "author", "created_at", "updated_at"]
    search_fields = ["title", "author__username"]
    list_filter = ["created_at"]
    ordering = ["-created_at"]


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('title', 'parent')
    list_filter = ('parent',)
    search_fields = ('title',)
    prepopulated_fields = {'title': ('title',)}
