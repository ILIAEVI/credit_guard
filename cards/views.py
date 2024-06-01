from rest_framework import generics, status, filters, permissions
from rest_framework.response import Response
from cards.models import Card
from cards.serializers import CardSerializer, AddCardSerializer


class CardListView(generics.ListAPIView):
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


class CardCreateView(generics.CreateAPIView):
    queryset = Card.objects.none()
    serializer_class = AddCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
