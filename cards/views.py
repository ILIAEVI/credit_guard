from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response

from cards.models import Card
from cards.serializers import CardSerializer, AddCardSerializer
from rest_framework.decorators import action


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all().order_by('-id')
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Card.objects.filter(user=user)
        else:
            return Card.objects.none()

    @action(
        methods=['post'],
        detail=False,
        url_path='add-card',
        serializer_class=AddCardSerializer,
        permission_classes=[]
    )
    def add_card(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
