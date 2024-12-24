from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription, Payment
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from .paginators import CustomPagination
from .services import (create_stripe_product, create_stripe_price,
                       create_stripe_session)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .tasks import send_course_update_email

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="Create a new course",
        responses={201: CourseSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a course",
        responses={200: CourseSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a course",
        responses={200: CourseSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a course",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        update_message = f"Курс '{instance.name}' был обновлен."
        send_course_update_email.delay(instance.id, update_message)

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="Create a new lesson",
        responses={201: LessonSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="List all lessons",
        responses={200: LessonSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a lesson",
        responses={200: LessonSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a lesson",
        responses={200: LessonSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a lesson",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Manage course subscription",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                            description='ID of the course'),
            },
            required=['course_id']
        ),
        responses={200: 'Subscription managed successfully'}
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                            description='ID of the course'),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER,
                                         description='Amount to pay'),
                'success_url': openapi.Schema(type=openapi.TYPE_STRING,
                                              description='Success URL'),
                'cancel_url': openapi.Schema(type=openapi.TYPE_STRING,
                                             description='Cancel URL'),
            },
            required=['course_id', 'amount', 'success_url', 'cancel_url']
        ),
        responses={201: 'Payment created successfully'}
    )
    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        amount = request.data.get('amount')
        success_url = request.data.get('success_url')
        cancel_url = request.data.get('cancel_url')

        # Создание продукта и цены в Stripe
        product = create_stripe_product(name=f"Course {course_id}")
        price = create_stripe_price(product_id=product.id, amount=amount)

        # Создание сессии для оплаты
        session = create_stripe_session(price_id=price.id,
                                        success_url=success_url,
                                        cancel_url=cancel_url)

        # Сохранение платежа в базе данных
        payment = Payment.objects.create(
            user=request.user,
            course_id=course_id,
            amount=amount,
            stripe_session_id=session.id,
            stripe_payment_intent_id=session.payment_intent,
        )

        return Response({'payment_url': session.url},
                        status=status.HTTP_201_CREATED)
