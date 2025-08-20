from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ────────────────────── EVENT CORE ────────────────────── #

# ✅ Defines event categories (e.g. tech, business)
class EventCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ✅ Main event object
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# ✅ Represents sessions within an event (e.g. breakout talks)
class Session(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    speaker = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title} - {self.event.title}"


# ✅ Sponsors supporting the event
class Sponsor(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='sponsors/')

    def __str__(self):
        return f"{self.name} - {self.event.title}"


# ────────────────────── PARTICIPANTS ────────────────────── #

# ✅ Links event participants to Django users
class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username if self.user else self.name} ({self.email})"



# ✅ Tracks attendance to specific sessions
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} attending {self.event.title}"



# ✅ Tickets booked by participants
class Ticket(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=100)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.name} - {self.ticket_type}"


# ────────────────────── FEEDBACK / RATING ────────────────────── #

# ✅ Feedback submitted by attendees
class Feedback(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.name} - {self.event.title}"


# ✅ Session-specific rating by attendees
class SessionRating(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.session.title} - {self.rating}"


# ────────────────────── GAMIFICATION ────────────────────── #

# ✅ Rewards earned by participants
class GamificationBadge(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.name} - {self.name}"


# ✅ Leaderboard ranking for participants
class LeaderboardEntry(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.participant.name} - {self.points} pts"


# ────────────────────── VENDORS / SERVICES ────────────────────── #

# ✅ Vendors offering services for the event
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    service_description = models.TextField()

    def __str__(self):
        return self.name


# ✅ Orders placed by participants to vendors
class ServiceOrder(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    service_requested = models.CharField(max_length=255)
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.participant.name} - {self.vendor.name} - {self.status}"


# ────────────────────── COMMUNICATIONS ────────────────────── #

# ✅ Messages sent by participants or vendors
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255, default='General')
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.recipient} - {self.subject}"
