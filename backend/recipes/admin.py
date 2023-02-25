from django.contrib import admin
from django.db.models import Count

from .models import (FavoriteRecipe, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)

@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    empty_value_display = '---'

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'text', 'pub_date', 'favorite_count'
    )
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name',)
    empy_value_display = '---'

    def favorite_count(self, obj):
        return obj.obj_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            obj_count=Count('favorite_recipe', distinct=True),
        )
    
    favorite_count.short_description = "Количество добавлений в избранное"

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'measurement_unit'
    )
    list_filter = ('name',)
    empy_value_display = '---'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'color', 'slug'
    )
    list_filter = ('name', 'slug')
    empy_value_display = '---'

@admin.register(FavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'favorite_recipe'
    )
    list_filter = ('id', 'user', 'favorite_recipe')
    empy_value_display = '---'

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'recipe'
    )
    list_filter = ('user', 'recipe')
    empy_value_display = '---'