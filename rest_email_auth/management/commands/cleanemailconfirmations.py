from django.core import management
from django.utils import timezone

from rest_email_auth import app_settings, models


class Command(management.BaseCommand):
    """
    Command to clean up old email confirmations.
    """

    help = "Clean up expired email confirmations."

    def handle(self, *args, **kwargs):
        """
        Handle execution of the command.
        """
        cutoff = timezone.now()
        cutoff -= app_settings.CONFIRMATION_EXPIRATION
        cutoff -= app_settings.CONFIRMATION_SAVE_PERIOD

        queryset = models.EmailConfirmation.objects.filter(
            created_at__lte=cutoff
        )

        count = queryset.count()

        queryset.delete()

        if count:
            self.stdout.write(
                self.style.SUCCESS(
                    "Removed {count} old email confirmation(s)".format(
                        count=count
                    )
                )
            )
        else:
            self.stdout.write("No email confirmations to remove.")
