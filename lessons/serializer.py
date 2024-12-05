from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lessons.models import Lesson, Course, Subscription
from lessons.validators import YoutubeValidators


class LessonSerializer(ModelSerializer):
    validators = [YoutubeValidators(field='video_url')]

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    lessons = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    def get_lessons(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, lesson):
        return Lesson.objects.filter.count(course=lesson.course)

    class Meta:
        model = Course
        fields = ('name', 'description', 'lessons_count')


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
