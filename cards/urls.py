from django.urls import path
from cards.views import CardListView, CardCreateView

urlpatterns = [
    path('cards/', CardListView.as_view(), name='card-list'),
    path('cards/create/', CardCreateView.as_view(), name='card-create')
]
