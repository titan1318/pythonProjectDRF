from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import CourseViewSet, LessonViewSet, RatingViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'payments', PaymentViewSet, basename='payment')

courses_router = NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'lessons', LessonViewSet, basename='course-lessons')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
]
