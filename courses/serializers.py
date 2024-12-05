from rest_framework import serializers
from .models import Lesson, Course, Subscription, Rating, Payment
from .validators import ExternalLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[ExternalLinkValidator(allowed_domains=["youtube.com"])]
    )

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video_url', 'course']


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'subscribed_at']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'course', 'score']

    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'course', 'amount', 'payment_date']
        read_only_fields = ['payment_date']
