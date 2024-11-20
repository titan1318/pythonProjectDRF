from rest_framework import viewsets, generics, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Count, Avg
from .models import Course, Lesson, Rating
from .permissions import IsAdminOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user', 'course']
    search_fields = ['user__username', 'course__title']

# Сериализатор для уроков
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course']


# Сериализатор для курсов
class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField(read_only=True)  # Поле creator

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lessons', 'lesson_count', 'average_rating', 'creator']
        read_only_fields = ['creator']

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_average_rating(self, obj):
        avg_score = obj.ratings.aggregate(avg_score=Avg('score'))['avg_score']
        return avg_score or 0


# ViewSet для курсов
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['lesson_count', 'average_rating']  # Поля для сортировки
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Аннотирование количества уроков и среднего рейтинга
        queryset = queryset.annotate(
            lesson_count=Count('lessons'),
            average_rating=Avg('ratings__score')
        )

        # Фильтрация по количеству уроков
        min_lessons = self.request.query_params.get('min_lessons')
        max_lessons = self.request.query_params.get('max_lessons')
        if min_lessons:
            queryset = queryset.filter(lesson_count__gte=min_lessons)
        if max_lessons:
            queryset = queryset.filter(lesson_count__lte=max_lessons)

        # Фильтрация по среднему рейтингу
        min_avg_rating = self.request.query_params.get('min_avg_rating')
        max_avg_rating = self.request.query_params.get('max_avg_rating')
        if min_avg_rating:
            queryset = queryset.filter(average_rating__gte=min_avg_rating)
        if max_avg_rating:
            queryset = queryset.filter(average_rating__lte=max_avg_rating)

        return queryset


# ViewSet для уроков
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        if not Course.objects.filter(id=course_id).exists():
            raise NotFound("Курс с таким ID не найден.")
        return Lesson.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(id=course_id)
        serializer.save(course=course)


# API для рейтингов
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'course', 'user', 'score']
        read_only_fields = ['user']


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ListCreateView и RetrieveUpdateDestroyView для уроков (по желанию)
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['course', 'title']
    search_fields = ['description']
    permission_classes = [IsAuthenticatedOrReadOnly]


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
