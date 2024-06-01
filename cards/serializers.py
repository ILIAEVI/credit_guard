from django.db import IntegrityError
from rest_framework import serializers
from cards.models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'title', 'censored_number', 'is_valid']
        read_only_fields = ['id', 'title', 'censored_number', 'is_valid']


class AddCardSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(max_length=16, required=True, write_only=True)
    ccv = serializers.IntegerField(min_value=100, max_value=999, required=True, write_only=True)

    class Meta:
        model = Card
        fields = ['title', 'card_number', 'ccv']

    def validate(self, attrs):
        card_number = attrs.get('card_number')
        if not card_number.isnumeric():
            raise serializers.ValidationError("Card number must be an integer!")
        if len(card_number) != 16:
            raise serializers.ValidationError("Card number must be 16 digits long!")
        ccv = attrs.get('ccv')
        # parts = [int(card_number[i:i+2]) for i in range(0, len(card_number), 2)]
        # pairs = [(parts[i], parts[i+1]) for i in range(0, len(parts), 2)]
        pairs_list = [(int(card_number[i:i+2]), int(card_number[i+2:i+4])) for i in range(0, len(card_number), 4)]

        is_valid = True
        for x, y in pairs_list:
            prod = x ** (y ** 3)
            if (prod % ccv) % 2 != 0:
                is_valid = False
                break
        attrs['is_valid'] = is_valid
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        card_number = validated_data.pop('card_number')
        censored_number = card_number[:4] + '*' * (len(card_number)-8) + card_number[-4:]
        validated_data['censored_number'] = censored_number
        validated_data['user'] = user
        validated_data.pop('ccv')
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError("You already have a card with this title.")

