from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from .models import Lesson
from .models import Payment
from rest_framework import serializers
from .models import Course, Lesson, Rating, Payment



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    creator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lessons', 'lesson_count', 'average_rating', 'creator']

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_average_rating(self, obj):
        avg_score = obj.ratings.aggregate(avg_score=models.Avg('score'))['avg_score']
        return avg_score or 0


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'course', 'user', 'score']
        read_only_fields = ['user']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'course', 'amount', 'payment_date']
        read_only_fields = ['user']
