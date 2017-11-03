"""Admin configurations for the ``rest_email_auth`` app.
"""

from django.contrib import admin

from rest_email_auth import models


@admin.register(models.EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    """
    Admin for ``EmailAddress`` instances.
    """
    fields = ('user', 'email', 'is_verified', 'created_at')
    list_display = ('email', 'user', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    readonly_fields = ('created_at',)
    search_fields = ('email',)


@admin.register(models.EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    """
    Admin for ``EmailConfirmation`` instances.
    """
    fields = ('email', 'key', 'created_at')
    list_display = ('email', 'created_at')
    readonly_fields = ('email', 'key', 'created_at')
    search_fields = ('email__email',)
