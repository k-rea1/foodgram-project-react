from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин'
        )
    
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='E-mail'
        )
    
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя')
    
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}'
    

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription')]