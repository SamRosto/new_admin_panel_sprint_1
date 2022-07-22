from django.contrib import admin
from . models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork

@admin.register(Genre)
class Genre(admin.ModelAdmin):
    pass


# @admin.register(Filmwork)
# class Filmwork(admin.ModelAdmin):
#     pass


@admin.register(Person)
class Person(admin.ModelAdmin):
    pass


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


# class PersonFilmworkInline(admin.TabularInline):
#     model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    list_display = ('title', 'type', 'creation_date', 'rating',)
    
    # filter by type
    list_filter = ('type', 'rating', 'creation_date')
    
    # Search by fields
    search_fields = ('title', 'description', 'id') 


