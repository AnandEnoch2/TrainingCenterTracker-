from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

# This will capture the login event
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    print(f"User {user.username} logged in")
    # You can perform other tasks here, such as logging the login time, etc.
