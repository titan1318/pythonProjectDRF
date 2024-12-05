from .serializers import CourseSerializer, LessonSerializer, RatingSerializer, PaymentSerializer
from .permissions import IsAdminOrModeratorEditOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Subscription, Course, Lesson, Rating, Payment
from .paginators import CustomPagination


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Проверяем подписку
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if not created:
            subscription.delete()
            message = "Subscription removed"
        else:
            message = "Subscription added"

        return Response({"message": message})


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['lesson_count', 'average_rating']
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAdminOrModeratorEditOnly]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, creator=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff and not self.request.user.groups.filter(name="Модераторы").exists():
            queryset = queryset.filter(creator=self.request.user)
        return queryset


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления уроками.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'create':  # Создавать могут только аутентифицированные пользователи
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:  # Админы/модераторы могут редактировать
            self.permission_classes = [IsAdminOrModeratorEditOnly]
        else:  # По умолчанию: только просмотр
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """
        При создании урока автоматически устанавливаем текущего пользователя как создателя.
        """
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        """
        Ограничиваем список объектов для обычных пользователей (не модераторов и не админов).
        """
        queryset = super().get_queryset()
        if not self.request.user.is_staff and not self.request.user.groups.filter(name="Модераторы").exists():
            # Только свои уроки
            queryset = queryset.filter(creator=self.request.user)
        return queryset

    def perform_update(self, serializer):
        # Обновление урока с указанием текущего пользователя
        serializer.save(creator=self.request.user)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
