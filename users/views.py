from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter

from users.models import CustomUser, Payment
from users.serializers import CustomUserSerializer, PaymentSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class UserListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields  = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']

    def perform_create(self, serializer):
        try:
            payment = serializer.save(user=self.request.user)

            product_name = payment.paid_course.name if payment.paid_course else payment.paid_lesson.name

            product = create_stripe_product(product_name)
            price = create_stripe_price(product, payment.payment_amount)
            session = create_stripe_session(price)

            payment.session_id = session.get('id')
            payment.payment_url = session.get('url')
            payment.product_id = product.get('id')
            payment.price_id = price.get('id')
            payment.save()
        except Exception as e:
            raise ValidationError(f"Ошибка при создании сессии оплаты: {str(e)}")


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()