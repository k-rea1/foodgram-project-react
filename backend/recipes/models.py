from django.db import models
from django.core.validators import MinValueValidator
from users.models import User

class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Наименование тега'
        )

    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цветовой HEX-код'
        )

    slug = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name='Слаг тега'
        )

    class Meta:
            verbose_name = 'Тег'
            verbose_name_plural = 'Теги'

    

class Ingredient(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Наименование ингредиента')
    
    measurement_unit = models.CharField(max_length=50,
                                        verbose_name='Ед. измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        
class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
        )
    
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
        )
    
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингредиенты'
        )
    
    name = models.CharField(
        max_length=200,
        verbose_name='Название')
    
    image = models.ImageField(
        upload_to='recipes/images',
        verbose_name='Изображение')
    
    text = models.TextField(
        verbose_name='Текст рецепта'
        )
    
    cooking_time = models.PositiveIntegerField(
        'Время готовки',
        default=1,
        validators=(MinValueValidator(1, 'Минимум 1 минута'),)
        )
    
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )


    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date',]
        
class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='amounts'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='amounts',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1,
        validators=(MinValueValidator(1, 'Минимум 1'),),
    )


    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [models.UniqueConstraint(fields=('recipe', 'ingredient'),
                                               name='unique ingredient')]
        
class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Рецепт',
    )


    class Meta:
        verbose_name = 'Избравнный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'favorite_recipe'),
                name='unique_favorite')]
        
class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_shopping_cart',
        verbose_name='Рецепт'
    )


    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique recipe in shopping cart')]

