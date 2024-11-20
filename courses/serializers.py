from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from .models import Course, Lesson, Rating
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'course', 'amount', 'payment_date']
        read_only_fields = ['user']



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'creator', 'lessons', 'lesson_count', 'average_rating']
        read_only_fields = ['creator']

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    def get_average_rating(self, obj):
        avg_score = obj.ratings.aggregate(avg_score=Avg('score'))['avg_score']
        return avg_score or 0

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
