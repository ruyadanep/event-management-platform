from django.contrib import admin
from .models import (
    Event, Session, EventCategory, Sponsor, Participant, Attendance, Ticket, 
    Feedback, SessionRating, GamificationBadge, LeaderboardEntry, Vendor, 
    ServiceOrder, Message
)

# ──────────────────────────────── INLINE MODELS ──────────────────────────────── #

# 🔁 Inline Sessions within Events
class SessionInline(admin.TabularInline):
    model = Session
    extra = 1

# 🔁 Inline Tickets within Participants
class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0

# ──────────────────────────────── ADMIN REGISTRATIONS ──────────────────────────────── #




@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'event', 'start_date', 'end_date']
    list_filter = ['event']
    search_fields = ['title', 'speaker']


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']




@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'name']
    list_filter = ['event']
    search_fields = ['name']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'event']
    list_filter = ['event']
    search_fields = ['name', 'email']
    inlines = [TicketInline]  # ✅ Show participant's tickets inline


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'timestamp']


#@admin.register(Attendance)
#class AttendanceAdmin(admin.ModelAdmin):
 #   list_display = ['user', 'event', 'timestamp']



@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant', 'ticket_type', 'purchase_date']
    list_filter = ['ticket_type']
    search_fields = ['participant__name']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'participant', 'submitted_at']
    list_filter = ['event']
    search_fields = ['participant__name']
    readonly_fields = ['submitted_at']


@admin.register(SessionRating)
class SessionRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'participant', 'rating']
    list_filter = ['rating']
    search_fields = ['session__title']


@admin.register(GamificationBadge)
class GamificationBadgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant', 'name', 'earned_at']
    list_filter = ['name']
    readonly_fields = ['earned_at']


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant', 'points']
    list_filter = ['points']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'service_description']
    search_fields = ['name']


# 🔘 Custom Admin Action for ServiceOrder
@admin.action(description="Mark selected orders as completed")
def mark_completed(modeladmin, request, queryset):
    queryset.update(status='completed')

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant', 'vendor', 'service_requested', 'status']
    list_filter = ['vendor', 'status']
    search_fields = ['service_requested']
    actions = [mark_completed]  # ✅ Bulk action
    fieldsets = (
        ('Participant & Vendor', {
            'fields': ('participant', 'vendor')
        }),
        ('Order Details', {
            'fields': ('service_requested', 'status')
        }),
    )  # ✅ Group fields in admin form


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'sent_at')
    search_fields = ('sender__username', 'recipient__username', 'subject')
    list_filter = ('sent_at',)



    def rsvp_count(self, obj):
        return obj.attendance_set.count()
    rsvp_count.short_description = 'Total RSVPs'

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    readonly_fields = ('participant', 'timestamp')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'start_date', 'end_date']
    list_filter = ['category', 'start_date']
    search_fields = ['title', 'location', 'description']
    inlines = [SessionInline, Attendance, AttendanceInline]  # ✅ Show related sessions inline
   