from core.models import AuthUser


def random_event():
    """Generate a random event."""
    for user in AuthUser.objects.all():
        print(user.username)
