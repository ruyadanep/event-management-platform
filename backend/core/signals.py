from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import Participant, Event

@receiver(post_save, sender=User)
def create_participant(sender, instance, created, **kwargs):
    if created and not Participant.objects.filter(user=instance).exists():
        # Assign first event (or use logic to choose)
        event = Event.objects.first()
        Participant.objects.create(user=instance, name=instance.username, email=instance.email, event=event)



@receiver(post_save, sender=User)
def create_participant_for_new_user(sender, instance, created, **kwargs):
    if created:
        # ✅ Try to find the next upcoming event
       
        upcoming_event = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date').first()


        # ✅ Assign it to the participant if it exists
        Participant.objects.get_or_create(
            user=instance,
            defaults={'event': upcoming_event}
        )
