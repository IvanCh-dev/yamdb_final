from django.contrib import admin
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


class GenreInline(admin.TabularInline):
    model = Title.genre.through


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name__startswith', )
    empty_value_display = ('-пусто-')
    ordering = ('name', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name__startswith', )
    empty_value_display = ('-пусто-')
    ordering = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'year')
    search_fields = ('name__startswith', 'gerne', 'category', 'year')
    empty_value_display = ('-пусто-')
    exclude = ('genre', )
    inlines = (
        GenreInline,
    )

    class Meta:
        ordering = ('name', 'genre', 'category')


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    search_fields = ('title__startswith', 'genre__startswith',)
    empty_value_display = ('-пусто-')
    ordering = ('title', 'genre')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'title', 'score', 'pub_date')
    search_fields = ('text__startswith',)
    empty_value_display = ('-пусто-')
    ordering = ('title', '-pub_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'review', 'pub_date')
    search_fields = ('text__startswith',)
    empty_value_display = ('-пусто-')
    ordering = ('review', '-pub_date')


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(TitleGenre, TitleGenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
