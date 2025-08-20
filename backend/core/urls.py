from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from .views import user_profile
from .views import unread_message_count
from .views import delete_message
from .views import cancel_rsvp, create_rsvp
from .views import MessageCreateView, MessageListView
from . views import sent_messages
from .views import list_users
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

from .views import UserRSVPListView

from core.views import (
    EventViewSet, SessionViewSet, EventCategoryViewSet, SponsorViewSet,
    ParticipantViewSet, AttendanceViewSet, TicketViewSet,
    FeedbackViewSet, SessionRatingViewSet, GamificationBadgeViewSet,
    LeaderboardEntryViewSet, VendorViewSet, ServiceOrderViewSet, MessageViewSet,
    RegisterView, LoginView, AttendanceCreateView
)

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

schema_view = get_schema_view(
    openapi.Info(
        title="EventHive API",
        default_version='v1',
        description="Interactive documentation for the EventHive platform.",
        contact=openapi.Contact(email="support@eventhive.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # ✅ Single attendance route
    path('api/v1/attendance/', UserRSVPListView.as_view(), name='user-rsvp-list'),
    path('attendance/', AttendanceCreateView.as_view(), name='attendance-create'),

   path("profile/", user_profile, name="user-profile"),

   path('messages/send/', MessageCreateView.as_view(), name='send-message'),
   path('messages/inbox/', MessageListView.as_view(), name='inbox'),
   path("messages/unread-count/", unread_message_count, name="unread-count"),
   path("messages/delete/<int:pk>/", delete_message, name="delete-message"),

   path("attendance/cancel/<int:pk>/", cancel_rsvp, name="cancel-rsvp"),
   path("attendance/rsvp/", create_rsvp, name="create-rsvp"),


   


   path("messages/sent/", sent_messages, name="sent-messages"),

   path("users/", list_users, name="list-users"),







    # ✅ Swagger docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# ✅ Static file serving in dev mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
