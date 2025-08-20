from rest_framework import viewsets, status
from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from core.models import (
    Event, Session, EventCategory, Sponsor, Attendance,
    Ticket, Participant, Feedback,
    SessionRating, GamificationBadge, LeaderboardEntry, Vendor,
    ServiceOrder, Message
)

from core.serializers import (
    EventSerializer, SessionSerializer, EventCategorySerializer, SponsorSerializer,
    ParticipantSerializer, AttendanceSerializer, TicketSerializer,
    FeedbackSerializer, SessionRatingSerializer,
    GamificationBadgeSerializer, LeaderboardEntrySerializer,
    VendorSerializer, ServiceOrderSerializer, MessageSerializer,
    RegisterSerializer
)

# ──────────────── EVENT MANAGEMENT ────────────────

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]


class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [IsAdminUser]


class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsAdminUser]


# ──────────────── PARTICIPANTS & ATTENDANCE ────────────────

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AttendanceCreateView(generics.CreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]




# ──────────────── TICKETS ────────────────

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(participant__user=self.request.user)

    def perform_create(self, serializer):
        participant = Participant.objects.get(user=self.request.user)
        serializer.save(participant=participant)


# ──────────────── FEEDBACK ────────────────

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Feedback.objects.all()
        return Feedback.objects.filter(participant__user=self.request.user)

    def perform_create(self, serializer):
        participant = Participant.objects.get(user=self.request.user)
        serializer.save(participant=participant)


class SessionRatingViewSet(viewsets.ModelViewSet):
    queryset = SessionRating.objects.all()
    serializer_class = SessionRatingSerializer
    permission_classes = [IsAuthenticated]


# ──────────────── GAMIFICATION ────────────────

class GamificationBadgeViewSet(viewsets.ModelViewSet):
    queryset = GamificationBadge.objects.all()
    serializer_class = GamificationBadgeSerializer
    permission_classes = [IsAuthenticated]


class LeaderboardEntryViewSet(viewsets.ModelViewSet):
    queryset = LeaderboardEntry.objects.all()
    serializer_class = LeaderboardEntrySerializer
    permission_classes = [IsAuthenticated]


# ──────────────── MARKETPLACE ────────────────

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]


class ServiceOrderViewSet(viewsets.ModelViewSet):
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
    permission_classes = [IsAuthenticated]


# ──────────────── MESSAGES ────────────────

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)
    

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


def get_queryset(self):
    # ✅ Mark all as read for the logged-in user
    unread = Message.objects.filter(recipient=self.request.user, is_read=False)
    unread.update(is_read=True)
    return Message.objects.filter(recipient=self.request.user).order_by('-sent_at')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_message_count(request):
    count = Message.objects.filter(recipient=request.user, is_read=False).count()
    return Response({"unread": count})

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sent_messages(request):
    class MessageSerializer(serializers.ModelSerializer):
        recipient_username = serializers.CharField(source='recipient.username', read_only=True)

        class Meta:
            model = Message
            fields = ['id', 'recipient_username', 'subject', 'body', 'sent_at']

    messages = Message.objects.filter(sender=request.user).order_by('-sent_at')
    serialized = MessageSerializer(messages, many=True)
    return Response(serialized.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_message(request, pk):
    try:
        message = Message.objects.get(pk=pk)

        if request.user != message.sender and request.user != message.recipient:
            return Response({'detail': 'Not authorized.'}, status=403)

        message.delete()
        return Response({'detail': 'Message deleted.'})

    except Message.DoesNotExist:
        return Response({'detail': 'Message not found.'}, status=404)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_rsvp(request, pk):
    try:
        rsvp = Attendance.objects.get(pk=pk, participant=request.user)
        rsvp.delete()
        return Response({'detail': 'RSVP cancelled successfully.'})
    except Attendance.DoesNotExist:
        return Response({'detail': 'RSVP not found or not yours.'}, status=404)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_rsvp(request):
    event_id = request.data.get('event')
    if not event_id:
        return Response({'error': 'Event ID required'}, status=400)

    try:
        event = Event.objects.get(id=event_id)
        Attendance.objects.create(participant=request.user, event=event)
        return Response({'detail': 'RSVP successful'})
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=404)


# ──────────────── AUTH / REGISTER / LOGIN ────────────────

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#class LoginView(APIView):
 #   permission_classes = [AllowAny]

  #  def post(self, request):
   #     username = request.data.get("username")
    #    password = request.data.get("password")
     #   user = authenticate(username=username, password=password)
      #  if user:
       #     token, _ = Token.objects.get_or_create(user=user)
        #    return Response({'token': token.key})
        #r#eturn Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    return Response({
        "username": request.user.username,
        "email": request.user.email,
        "id": request.user.id
    })




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username']

    users = User.objects.exclude(id=request.user.id)
    serialized = UserSerializer(users, many=True)
    return Response(serialized.data)





# ──────────────── RSVP HISTORY ────────────────

class UserRSVPListView(ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # ✅ Use actual field names from Event model
    search_fields = ['event__title', 'event__description']
    ordering_fields = ['event__start_date', 'event__end_date']
    filterset_fields = ['event']

    def get_queryset(self):
        return Attendance.objects.filter(user=self.request.user).select_related('event')


