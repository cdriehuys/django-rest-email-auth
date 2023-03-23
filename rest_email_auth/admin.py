"""Admin configurations for the ``rest_email_auth`` app.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_email_auth import models


@admin.register(models.EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    """
    Admin for ``EmailAddress`` instances.
    """

    fields = ("user", "email", "is_verified", "created_at")
    list_display = ("email", "user", "is_verified", "created_at")
    list_filter = ("is_verified",)
    readonly_fields = ("created_at",)
    search_fields = ("email",)


@admin.register(models.EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    """
    Admin for ``EmailConfirmation`` instances.
    """

    fields = ("email", "key", "created_at")
    list_display = ("email", "created_at")
    readonly_fields = ("email", "key", "created_at")
    search_fields = ("email__email",)


@admin.register(models.PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin for ``PasswordResetToken`` instances.
    """

    fields = ("email", "key", "created_at")
    list_display = ("get_user", "email", "created_at")
    readonly_fields = fields
    search_fields = (get_user_model().USERNAME_FIELD, "email__email")

    def get_user(self, obj):
        """
        Get the user that owns the password reset token.
        """
        return obj.email.user

    get_user.admin_order_field = "email__user"
    get_user.short_description = _("user")
