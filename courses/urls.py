from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import CourseViewSet, LessonViewSet, RatingViewSet, PaymentViewSet, SubscriptionView

# Основной роутер
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'payments', PaymentViewSet, basename='payment')

# Вложенный роутер для уроков в курсах
courses_router = NestedSimpleRouter(router, r'courses', lookup='course')
courses_router.register(r'lessons', LessonViewSet, basename='course-lessons')

# URL-адреса
urlpatterns = [
    path('', include(router.urls)),  # Основной роутер
    path('', include(courses_router.urls)),  # Вложенный роутер
    path('subscribe/', SubscriptionView.as_view(), name='course-subscribe'),
]
