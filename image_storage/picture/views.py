from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from rest_framework import status, generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Image, ExpiringLink
from .serializers import ImageUploadSerializer, ImageLinkSerializer, ExpiringLinkSerializer


class ImageUploadAndListByUserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Image.objects.all()
    serializer_class_create = ImageUploadSerializer
    serializer_class_list = ImageLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class_list
        elif self.action == 'create':
            return self.serializer_class_create
        return super().get_serializer_class()

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user_id = self.request.user.id
        return Image.objects.filter(user__id=user_id).prefetch_related('links')


class ExpiringLinkView(SingleObjectMixin, View):
    model = ExpiringLink

    def get(self, request, *args, **kwargs):
        short_url = kwargs['link']
        mapping = get_object_or_404(ExpiringLink, link=short_url)
        if mapping.is_expired():
            return Response({'error': 'Link Expired.'}, status=status.HTTP_404_NOT_FOUND)
        return redirect(f'http://0.0.0.0:8000/media/{mapping.image.image_file}')


class ExpiringLinkCreateView(generics.CreateAPIView):
    serializer_class = ExpiringLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"domain": self.request.META["HTTP_HOST"], "pk": self.kwargs.get('pk')}

    def create(self, request, *args, **kwargs):
        user_tier = request.user.tier
        pk = self.kwargs.get('pk')
        try:
            image = Image.objects.select_related('user').get(pk=pk)
            if image.user.id != request.user.id or not user_tier.expiring_link:
                return Response({'error': 'Access denied'},
                                status=status.HTTP_403_FORBIDDEN)

        except Image.DoesNotExist:
            return Response({'error': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            link = serializer.create(
                validated_data=serializer.validated_data
            )
            full_link = f"http://{self.request.META['HTTP_HOST']}/api/v1/expiration/{link}"

            return Response({'link': full_link}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
