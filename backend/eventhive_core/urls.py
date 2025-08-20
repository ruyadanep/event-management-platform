from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)





from core.views import (
    EventViewSet, SessionViewSet, EventCategoryViewSet, SponsorViewSet,
    ParticipantViewSet, AttendanceViewSet, TicketViewSet, FeedbackViewSet,
    SessionRatingViewSet, GamificationBadgeViewSet, LeaderboardEntryViewSet,
    VendorViewSet, ServiceOrderViewSet, MessageViewSet,
    RegisterView, LoginView
)

# ✅ DRF router setup
router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'categories', EventCategoryViewSet)
router.register(r'sponsors', SponsorViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'session-ratings', SessionRatingViewSet)
router.register(r'badges', GamificationBadgeViewSet)
router.register(r'leaderboard', LeaderboardEntryViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'services', ServiceOrderViewSet)
router.register(r'messages', MessageViewSet)

# ✅ Swagger schema config
schema_view = get_schema_view(
    openapi.Info(
        title="EventHive API",
        default_version='v1',
        description="EventHive Swagger UI",
        contact=openapi.Contact(email="support@eventhive.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)




urlpatterns = [
    # ✅ Admin panel
    path('admin/', admin.site.urls),
    path('api/v1/', include('core.urls')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ All API routes
    path('api/v1/', include(router.urls)),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/login/', LoginView.as_view(), name='login'),

    # ✅ Swagger docs (now renamed to avoid any conflict)
    path('api-redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
