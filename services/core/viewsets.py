
from .mixins import ActionSerializersViewSetMixin
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import (
    ViewSetMixin
)
from rest_framework import mixins


class GenericViewSet(ViewSetMixin, GenericAPIView):
    pass


class ModelViewSet(ActionSerializersViewSetMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    pass