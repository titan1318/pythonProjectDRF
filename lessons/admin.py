from django.contrib import admin
from lessons.models import Lesson, Course, Subscription


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'owner')
    list_filter = ('name', 'course',)
    search_fields = ('name', 'course', 'owner',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')
    list_filter = ('name', 'description',)
    search_fields = ('name', 'description', 'owner',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_subscribe')
    list_filter = ('user', 'course',)
    search_fields = ('user', 'course', 'is_subscribe',)