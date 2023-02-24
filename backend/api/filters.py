from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Ingredient

User = get_user_model()


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipesFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
        )
    
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        )
    
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
        )
    
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
        )

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'author', 'tags', 'is_in_shopping_cart']

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(
                recipe_shopping_cart__user=self.request.user)
        return queryset