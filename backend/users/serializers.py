from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from djoser.serializers import (PasswordSerializer, UserCreateSerializer,
                                UserSerializer)

from recipes.models import Recipe
from .models import Follow
from rest_framework import serializers

User = get_user_model()


class UserListSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed'
                  )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        required_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

class SetPasswordSerializer(PasswordSerializer):
    current_password = serializers.CharField(
        required=True,
        label='Текущий пароль')

    def validate(self, data):
        user = self.context.get('request').user
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError({
                "new_password": "Новый пароль должен отличаться от старого"})
        check_current = check_password(data['current_password'], user.password)
        if check_current is False:
            raise serializers.ValidationError({
                "current_password": "Неправильный пароль"})
        return data
    
class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

class FollowSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        source='author.email',
        read_only=True)
    id = serializers.IntegerField(
        source='author.id',
        read_only=True)
    username = serializers.CharField(
        source='author.username',
        read_only=True)
    first_name = serializers.CharField(
        source='author.first_name',
        read_only=True)
    last_name = serializers.CharField(
        source='author.last_name',
        read_only=True)
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(
        source='author.recipe.count')

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count',)

    def validate(self, data):
        user = self.context.get('request').user
        author = self.context.get('author_id')
        if user.id == int(author):
            raise serializers.ValidationError({
                'errors': 'Нельзя подписаться на самого себя'})
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError({
                'errors': 'Вы уже подписаны на данного пользователя'})
        return data

    def get_recipes(self, obj):
        recipes = obj.author.recipe.all()
        return SubscribeRecipeSerializer(
            recipes,
            many=True).data

    def get_is_subscribed(self, obj):
        subscribe = Follow.objects.filter(
            user=self.context.get('request').user,
            author=obj.author
        )
        if subscribe:
            return True
        return False