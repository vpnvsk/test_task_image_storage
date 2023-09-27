import hashlib
import random

from django.db import IntegrityError

from rest_framework import serializers, status

from rest_framework.response import Response

from picture.models import Image, Link, ExpiringLink


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['link', 'size']


class ImageLinkSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'image_file', 'links']

    def __init__(self, *args, **kwargs):
        super(ImageLinkSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        if not user.tier.original_link:
            self.fields.pop('image_file')


class ImageUploadSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'user', 'name', 'image_file', 'thumbnail_url']

    def __init__(self, *args, **kwargs):
        super(ImageUploadSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['user'].write_only = True
        if not user.tier.original_link:
            self.fields['image_file'].write_only = True

    def get_thumbnail_url(self, obj):
        return obj.create_thumbnail_links() if obj.image_file else None

    def get_user(self, obj):
        return obj.user.id

    def create(self, validated_data):

        thumbnail_urls = validated_data.pop('thumbnail_urls', None)

        instance = super().create(validated_data)

        if thumbnail_urls:
            for thumbnail_url in thumbnail_urls:
                Link.objects.create(
                    image=instance,
                    link=thumbnail_url,
                    size=200,
                )

        return instance


class ExpiringLinkSerializer(serializers.ModelSerializer):
    link = serializers.URLField(required=False)
    expiration_time = serializers.IntegerField(min_value=300, max_value=30000)

    class Meta:
        model = ExpiringLink
        fields = ['expiration_time', 'link']

    def create(self, validated_data):

        domain = self.context['domain']
        for i, j in validated_data.items():
            e_t = j
        pk = self.context['pk']
        link = f"{hashlib.shake_128(str(pk).encode('utf-8')).hexdigest(3).upper()}"
        existing_link = ExpiringLink.objects.filter(link=link)
        if existing_link.exists():
            char_list = list(link)
            random.shuffle(char_list)
            link = ''.join(char_list)

        try:
            ExpiringLink.objects.create(image=Image.objects.get(id=pk), link=link,
                                        expiration_time=e_t)
        except IntegrityError:
            return Response({'error': 'Integrity error.'}, status=status.HTTP_400_BAD_REQUEST)

        return link
