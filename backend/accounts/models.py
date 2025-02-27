from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modelo de usuário personalizado que estende o AbstractUser do Django.
    Adiciona flags para diferentes tipos de usuários no sistema.
    """
    is_analyst = models.BooleanField(default=False, verbose_name="É Analista")
    is_manager = models.BooleanField(default=False, verbose_name="É Gerente")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username