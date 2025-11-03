from rest_framework import serializers

from .models import CustomUser, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def validate_payment_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма платежа должна быть больше 0.")
        return value

    def validate(self, data):
        paid_course = data.get('paid_course')
        paid_lesson = data.get('paid_lesson')

        if not paid_course and not paid_lesson:
            raise serializers.ValidationError(
                "Укажите, за что вы хотите оплатить. За курс или урок."
            )
        if paid_course and paid_lesson:
            raise serializers.ValidationError(
                "Можно оплатить либо за курс, либо за урок."
            )
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number', 'avatar', 'country', 'payments',
        ]
