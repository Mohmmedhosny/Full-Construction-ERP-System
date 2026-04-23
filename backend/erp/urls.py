from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/resources/', include('resources.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/procurement/', include('procurement.urls')),
    path('api/hr/', include('hr.urls')),
    path('api/documents/', include('documents.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add token auth endpoint for local testing
try:
    from rest_framework.authtoken.views import obtain_auth_token
    urlpatterns += [path('api/token/', obtain_auth_token, name='api_token_auth')]
except Exception:
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    urlpatterns += [
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
