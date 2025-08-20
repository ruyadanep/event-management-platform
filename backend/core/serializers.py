from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import (
    Event, Session, EventCategory, Sponsor, Participant, Attendance, Ticket,
    Feedback, SessionRating, GamificationBadge, LeaderboardEntry, Vendor, ServiceOrder, Message
)

# ────────────────────── EVENT SERIALIZERS ────────────────────── #

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


# ────────────────────── PARTICIPANT / ATTENDANCE ────────────────────── #

class ParticipantSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # shows username

    class Meta:
        model = Participant
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'event', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)




# ────────────────────── TICKETING ────────────────────── #

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


# ────────────────────── FEEDBACK / RATING ────────────────────── #

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class SessionRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionRating
        fields = '__all__'


# ────────────────────── GAMIFICATION ────────────────────── #

class GamificationBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamificationBadge
        fields = '__all__'

class LeaderboardEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderboardEntry
        fields = '__all__'


# ────────────────────── MARKETPLACE ────────────────────── #

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class ServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = '__all__'


# ────────────────────── MESSAGING ────────────────────── #

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'recipient', 'recipient_username', 'subject', 'body', 'sent_at']
        read_only_fields = ['sender', 'sent_at']


# ────────────────────── AUTH: REGISTRATION ────────────────────── #

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        Token.objects.create(user=user)

        # ✅ Auto-create linked Participant
        Participant.objects.create(
            user=user,
            name=user.username,
            email=user.email,
            event=Event.objects.first()  # ⛔ you can change this logic later
        )
        return user


class AttendanceSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'event']
