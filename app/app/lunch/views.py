"""
Views for the lunch APIs
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Place
from lunch import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'search',
                OpenApiTypes.STR,
                description='Search a place filtering by name and address',
            ),
            OpenApiParameter(
                'limit',
                OpenApiTypes.NUMBER,
                description='Limit the number of the places retrieved',
                default=1000
            ),
            OpenApiParameter(
                'offset',
                OpenApiTypes.NUMBER,
                description='Retrieve the places starting by an offset',
                default=0
            ),
        ]
    )
)
class PlaceViewSet(viewsets.ModelViewSet):
    """View for manage place APIs."""
    serializer_class = serializers.PlaceDetailSerializer
    queryset = Place.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve places for authenticated user."""
        queryset = self.queryset

        if self.action == 'list':
            search = self.request.query_params.get('search')
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) | Q(address__icontains=search)
                )

            str_offset = self.request.query_params.get('offset')
            offset = int(str_offset) if str_offset else 0

            str_limit = self.request.query_params.get('limit')
            limit = 1000
            if str_limit:
                int_limit = int(str_limit)
                if int_limit > 0 and int_limit < 1000:
                    limit = int_limit

            queryset = queryset.order_by('name')[offset:limit]

        return queryset

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.PlaceSerializer
        elif self.action == 'upload_image':
            return serializers.PlaceImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to place."""
        place = self.get_object()
        serializer = self.get_serializer(place, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
