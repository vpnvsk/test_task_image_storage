import os

from django.utils import timezone
from django.db import models
from PIL import Image as PILImage

from users.models import User


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    image_file = models.ImageField(upload_to='images/')
    added_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def create_thumbnail_links(self):
        thumbnail_urls = []
        for i in self.user.tier.thumbnail_size.all():

            thumbnail_height = i.size
            thumbnail_width = int(self.image_file.width * (thumbnail_height / self.image_file.height))
            thumbnail_filename = f"thumbnail/{i.size}.{os.path.basename(self.image_file.name)}"

            thumbnail_path = self.image_file.storage.path(thumbnail_filename)
            if not self.image_file.storage.exists(thumbnail_filename):
                image = PILImage.open(self.image_file.path)
                image.thumbnail((thumbnail_width, thumbnail_height), PILImage.LANCZOS)
                image.save(thumbnail_path)
            thumbnail_url = f'http://0.0.0.0:8000/media/{thumbnail_filename}'
            link = Link.objects.create(
                image=self,
                link=thumbnail_url,
                size=thumbnail_height
            )

            thumbnail_urls.append(link.link)

        return thumbnail_urls


class Link(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='links')
    link = models.URLField()
    size = models.IntegerField()


class ExpiringLink(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    expiration_time = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    link = models.URLField()

    class Meta:
        verbose_name = "Expiring Link"
        verbose_name_plural = "Expiring Links"

    def is_expired(self):
        expiration_timestamp = self.created_at + timezone.timedelta(seconds=self.expiration_time)
        return timezone.now() >= expiration_timestamp
