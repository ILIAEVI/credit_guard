from django.urls import path
from cards.views import CardListView, CardCreateView, BulkCreateCardView

urlpatterns = [
    path('cards/', CardListView.as_view(), name='card-list'),
    path('cards/create/', CardCreateView.as_view(), name='card-create'),
    path('cards/bulk-create/', BulkCreateCardView.as_view(), name='card-bulk-create'),
]
