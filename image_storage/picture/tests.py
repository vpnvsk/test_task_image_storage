import json

from django.core.files import File
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from picture.factory import ImageFactory
from picture.models import Image
from users.factory import ThumbnailFactory, TierFactory, UserFactory


class ImageUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.thumbnail = ThumbnailFactory()
        self.thumbnail2 = ThumbnailFactory(size=400)
        self.tier = TierFactory(thumbnail_size=(self.thumbnail, self.thumbnail2))
        self.user = UserFactory(tier=self.tier)
        refresh = RefreshToken.for_user(self.user)
        self.token = refresh.access_token

        # Set the Authorization header with the Bearer token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_image_upload(self):

        image_path = 'media/images/IMG-20230808-WA0001.jpg'
        with open(image_path, 'rb') as image_file:
            image_data = File(image_file, name='test_image.png')

            # Ensure the endpoint URL is correct
            url = '/api/v1/img/'

            # Make a POST request to upload the image
            response = self.client.post(url, {'image_file': image_data, 'name': 'Test Image'})

            # Verify the response status code (HTTP 201 Created)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Verify that an Image object was created in the database
            self.assertEqual(Image.objects.count(), 1)

            # Verify the details of the created Image object
            image = Image.objects.first()
            response_data = json.loads(response.content)

            self.assertEqual(len(response_data['thumbnail_url']), 2)
            self.assertEqual(image.user, self.user)
            self.assertEqual(image.name, 'Test Image')


class ImageListTest(TestCase):

    def setUp(self) -> None:
        self.client3 = APIClient()
        self.client = APIClient()
        self.client2 = APIClient()
        self.thumbnail = ThumbnailFactory()
        self.thumbnail2 = ThumbnailFactory(size=400)
        self.tier = TierFactory(thumbnail_size=(self.thumbnail,))
        self.tier1 = TierFactory(thumbnail_size=(self.thumbnail, self.thumbnail2), name='Premium', original_link=True)
        self.user = UserFactory(tier=self.tier, username='Bob')
        self.user2 = UserFactory(tier=self.tier1, username='Tom')
        self.image = ImageFactory.create_thumbnail_links(user=self.user)
        self.image2 = ImageFactory.create_thumbnail_links(user=self.user2)
        refresh = RefreshToken.for_user(self.user)
        self.token = refresh.access_token

        # Set the Authorization header with the Bearer token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        refresh2 = RefreshToken.for_user(self.user2)
        self.token2 = refresh2.access_token

        # Set the Authorization header with the Bearer token
        self.client2.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')

    def test_get_image_list(self):
        url = '/api/v1/gimg/'

        # Make a POST request to upload the image
        response = self.client.get(url)
        response2 = self.client2.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        response_data2 = json.loads(response2.content)
        self.assertEqual(len(response_data[0]['links']), 1)
        self.assertEqual(len(response_data2[0]['links']), 2)
        self.assertEqual(('image_file' in response_data2[0]), True)

    def test_error_request(self):
        url = '/api/v1/gimg/'
        response = self.client3.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetExpiringLinkTest(TestCase):
    def setUp(self) -> None:
        self.client3 = APIClient()
        self.client = APIClient()
        self.client2 = APIClient()
        self.thumbnail = ThumbnailFactory()
        self.thumbnail2 = ThumbnailFactory(size=400)
        self.tier = TierFactory(thumbnail_size=(self.thumbnail, self.thumbnail2), name='Premium', original_link=True)
        self.tier1 = TierFactory(thumbnail_size=(self.thumbnail, self.thumbnail2), name='Enterprise',
                                 original_link=True, expiring_link=True)
        self.user = UserFactory(tier=self.tier, username='Bob')
        self.user2 = UserFactory(tier=self.tier1, username='Tom')
        self.image = ImageFactory.create_thumbnail_links(user=self.user)
        self.image2 = ImageFactory.create_thumbnail_links(user=self.user2)
        refresh = RefreshToken.for_user(self.user)
        self.token = refresh.access_token

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        refresh2 = RefreshToken.for_user(self.user2)
        self.token2 = refresh2.access_token

        # Set the Authorization header with the Bearer token
        self.client2.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        self.url = '/api/v1/img/1/'
        custom_host = 'yourcustomdomain'

        # Modify the default settings for the test client
        self.client2.defaults['HTTP_HOST'] = custom_host

    def test_unauthorized(self):
        response = self.client3.post(self.url, {'expiration_time': 300})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_user(self):
        response = self.client.post(self.url, {'expiration_time': 300})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

















