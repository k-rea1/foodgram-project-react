from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                            Tag, IngredientAmount)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from django.db.models import Sum
from .filters import IngredientFilter, RecipesFilter
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .serializers import (IngredientSerializer, RecipeListSerializer,
                          RecipeEditSerializer, ShortRecipeSerializer,
                          TagSerializer,)

User = get_user_model()

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeEditSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = ShortRecipeSerializer(recipe, data=request.data,
                                          context={"request": request})
            serializer.is_valid(raise_exception=True)
            if not FavoriteRecipe.objects.filter(user=request.user,
                                           favorite_recipe=recipe).exists():
                FavoriteRecipe.objects.create(user=request.user,
                                              favorite_recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'errors': 'Рецепт уже добавлен в избранное'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            get_object_or_404(FavoriteRecipe, user=request.user,
                              favorite_recipe=recipe).delete()
            return Response({'detail': 'Рецепт удален из избранного'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            pagination_class=None)
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = ShortRecipeSerializer(recipe, data=request.data,
                                          context={"request": request})
            serializer.is_valid(raise_exception=True)
            if not ShoppingCart.objects.filter(user=request.user,
                                                recipe=recipe).exists():
                ShoppingCart.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'errors': 'Рецепт уже добавлен в список покупок'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            get_object_or_404(ShoppingCart, user=request.user,
                              recipe=recipe).delete()
            return Response(
                {'detail': 'Рецепт удален из списка покупок'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientAmount.objects
            .filter(recipe__recipe_shopping_cart__user=request.user)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list('ingredient__name', 'total_amount',
                         'ingredient__measurement_unit')
        )
        file_list = []
        [file_list.append(
            '{} - {} {}.'.format(*ingredient)) for ingredient in ingredients]
        file = HttpResponse('Cписок покупок:\n' + '\n'.join(file_list),
                            content_type='text/plain')
        file['Content-Disposition'] = (f'attachment; filename=list-to-buy.txt')
        return file

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filterset_class = IngredientFilter