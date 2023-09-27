import os
import django
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'image_storage.settings'
django.setup()
from users.factory import UserFactory, ThumbnailFactory, TierFactory

# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module


def populate_database():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'image_storage.settings'
    django.setup()
    # Create Thumbnail objects
    thumbnail1 = ThumbnailFactory()
    thumbnail2 = ThumbnailFactory(size=400)

    # Create Tier objects
    tier_basic = TierFactory(thumbnail_size=(thumbnail1,))
    tier_premium = TierFactory(thumbnail_size=(thumbnail1, thumbnail2), name='Premium', original_link=True)
    tier_enterprise = TierFactory(thumbnail_size=(thumbnail1, thumbnail2), name='Enterprise', original_link=True, expiring_link=True)

    # Create User objects
    basic_user = UserFactory(tier=tier_basic, username='basic')
    premium_user = UserFactory(tier=tier_premium, username='premium')
    enterprise_user = UserFactory(tier=tier_enterprise, username='enterprise')

if __name__ == "__main__":
    populate_database()

