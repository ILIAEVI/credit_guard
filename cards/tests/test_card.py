import random
import time
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse_lazy
from cards.models import Card


def generate_card_number():
    return ''.join(str(random.randint(0, 9)) for _ in range(16))


def generate_ccv():
    return random.randint(100, 999)


class TestCard(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)

    def test_validation_time(self):
        url = reverse_lazy('card-create')

        start_time = time.time()
        for _ in range(100):
            card_number = generate_card_number()
            ccv = generate_ccv()
            title = f"Card {_}"

            data = {'title': title, 'card_number': card_number, 'ccv': ccv}

            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        end_time = time.time()
        duration = end_time - start_time
        self.assertLess(duration, 0.5, f"Validation time is too long: {duration}")

    def test_time(self):
        url = reverse_lazy('card-bulk-create')
        start_time = time.time()
        cards_data = []

        for _ in range(100):
            card_number = generate_card_number()
            ccv = generate_ccv()
            title = f"Card {_}"
            data = {'title': title, 'card_number': card_number, 'ccv': ccv}
            cards_data.append(data)

        response = self.client.post(url, data=cards_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        end_time = time.time()
        duration = end_time - start_time
        self.assertLess(duration, 0.5, f"Validation time is too long: {duration}")

    def test_valid_card(self):
        url = reverse_lazy('card-create')

        card_number = '1234123412341234'
        ccv = 200
        title = f"Card test"

        valid_data = {'title': title, 'card_number': card_number, 'ccv': ccv}

        response = self.client.post(url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        card = Card.objects.get(user=self.user, title='Card test')
        self.assertTrue(card.is_valid)

    def test_invalid_card(self):
        url = reverse_lazy('card-create')
        card_number = '1145123412341234'
        title = f"Card"
        ccv = 125

        data = {'title': title, 'card_number': card_number, 'ccv': ccv}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        card = Card.objects.get(user=self.user, title='Card')
        self.assertFalse(card.is_valid)

    def test_invalid_card_length(self):
        url = reverse_lazy('card-create')
        card_number = '123245666'
        title = f"Card"
        ccv = generate_ccv()

        data = {'title': title, 'card_number': card_number, 'ccv': ccv}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_numeric_card(self):
        url = reverse_lazy('card-create')
        card_number = '123f123412341234'
        ccv = generate_ccv()
        title = f"Card"
        data = {'title': title, 'card_number': card_number, 'ccv': ccv}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
