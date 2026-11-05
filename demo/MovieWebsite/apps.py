from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_moderator_group(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from .models import Profile
    
    ct = ContentType.objects.get_for_model(Profile)
    perm, _ = Permission.objects.get_or_create(
        codename='can_block_users',
        content_type=ct,
        defaults={'name': 'Can block and unblock users'}
    )
    group, _ = Group.objects.get_or_create(name='Moderator')
    group.permissions.add(perm)

class MoviewebsiteConfig(AppConfig):
    name = 'MovieWebsite'

    def ready(self):
        from . import signals
        post_migrate.connect(create_moderator_group, sender=self)