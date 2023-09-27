import factory

from users.models import Thumbnail, Tier, User


class ThumbnailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thumbnail
        django_get_or_create = ('size',)

    size = 200


class TierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tier
    name = 'Basic'
    original_link = False
    expiring_link = False

    @factory.post_generation
    def thumbnail_size(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.thumbnail_size.add(*extracted)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = 'John'
    password = factory.django.Password('1234')
    tier = factory.SubFactory(TierFactory)

