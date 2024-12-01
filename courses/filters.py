from django_filters import rest_framework as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    min_lesson_count = filters.NumberFilter(method='filter_by_min_lesson_count')
    max_lesson_count = filters.NumberFilter(method='filter_by_max_lesson_count')

    class Meta:
        model = Course
        fields = []

    def filter_by_min_lesson_count(self, queryset, name, value):
        return queryset.annotate(lesson_count=models.Count('lessons')).filter(lesson_count__gte=value)

    def filter_by_max_lesson_count(self, queryset, name, value):
        return queryset.annotate(lesson_count=models.Count('lessons')).filter(lesson_count__lte=value)
