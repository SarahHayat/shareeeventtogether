from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser):
        if not email:
            raise ValueError('Un email est requis')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
        )
        if password:
            user.set_password(password)

        user.save()
        return user

    def create_user(self, email, password=None):
        return self._create_user(email, password, False, False)

    def create_superuser(self, email, password):
        return self._create_user(email, password, True, True)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email', max_length=254, unique=True)
    is_staff = models.BooleanField('statut staff', default=False)
    is_superuser = models.BooleanField('statut superutilisateur', default=False)
    is_active = models.BooleanField('actif', default=True)
    last_login = models.DateTimeField('dernière connexion', null=True, blank=True)
    date_joined = models.DateTimeField('date d\'inscription', auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['email', ]
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'

    def __str__(self):
        return self.email
