from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UsernameField
from django.forms import ModelForm

from users.models import User


class CustomUserCreationForm(ModelForm):

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD,)
        field_classes = {User.USERNAME_FIELD: UsernameField}


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email',)
            }
        ),
    )
    list_display = ('email', 'is_staff', 'last_login')
    ordering = ('email',)