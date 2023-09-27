import os

import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from factory import SubFactory

from picture.models import Image, Link
from users.factory import UserFactory


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    image_file = SimpleUploadedFile(
        "test_image.jpg", b"dummy_image_content", content_type="image/jpeg",
    )
    name = 'dumb name'
    user = factory.SubFactory(UserFactory)

    @classmethod
    def create_thumbnail_links(cls, user, **kwargs):
        thumbnail_urls = []
        image_instance = cls(image_file=cls.image_file, name=cls.name, user=user)
        image_instance.save()
        for i in user.tier.thumbnail_size.all():
            thumbnail_height = i.size
            thumbnail_width = int(400 * (thumbnail_height / 200))
            thumbnail_filename = f"thumbnail/{i.size}.{os.path.basename(cls.image_file.name)}"

            thumbnail_url = f'http://0.0.0.0:8000/media/{thumbnail_filename}'

            link = LinkFactory(image=image_instance, link=thumbnail_url, size=thumbnail_height)

            thumbnail_urls.append(link.link)

        return thumbnail_urls


class LinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Link

    image = SubFactory(ImageFactory)
    link = 'qwerty/asdfgh/sdfg.com'
    size = 200
