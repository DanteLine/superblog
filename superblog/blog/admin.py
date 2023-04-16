from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from blog.models import Post, Category, Author, MyTag
from django import forms
from django.contrib.auth.admin import UserAdmin, User

class UserAdminCustom(UserAdmin):
   list_display = ('id', 'username', 'is_staff', 'is_superuser')
   list_display_links = ('id', 'username')
   list_filter = ('is_staff', 'is_superuser')
   search_fields = ('username', )

admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    list_display = ('id', 'user', 'first_name', 'last_name', 'get_photo')
    list_display_links = ('id', 'first_name', 'last_name')
    save_as = True
    save_on_top = True

    def get_photo(self, obj):
        if obj.author_photo:
            return mark_safe(f"<img src={obj.author_photo.url} width=75>")



@admin.register(Post)
class PostAdmid(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'views', 'category',  'created_at', 'get_photo')
    list_display_links = ('title', )
    list_filter = ('category', 'tags')
    readonly_fields = ('created_at', 'get_photo')
    fields = ('title', 'slug', 'category','tags', 'photo', 'content', 'author', 'views', 'created_at', 'get_photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src={obj.photo.url} width=75>")

    get_photo.short_description = 'Фото'

@admin.register(MyTag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title', )}
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug')
    list_display_links = ('title', )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug': ('title',)}

