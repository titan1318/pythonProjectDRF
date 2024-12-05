from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from payments.views import StripePaymentView, StripeSessionStatusView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/payments/', include('payments.urls')),
    path('api/users/', include('users.urls')),
    path('api/payments/stripe/create/', StripePaymentView.as_view(), name='stripe-create'),
    path('api/payments/stripe/status/', StripeSessionStatusView.as_view(), name='stripe-status'),
    path('api/payments/stripe/create/', StripePaymentView.as_view(), name='stripe-create'),
    path('api/payments/stripe/status/', StripeSessionStatusView.as_view(), name='stripe-status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)