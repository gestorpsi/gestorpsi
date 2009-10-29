import datetime
from django.db import models
from django.conf import settings
from django.db.models import signals
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from gestorpsi.referral.models import Referral
from gestorpsi.schedule.models import ScheduleOccurrence

class MessageManager(models.Manager):
    """
    This is the manager for objects of the "Message" class. Messages are used
    in the "online messages" and "chat" services.
    """

    def messages_for(self, referral):
        """
        Returns all messages that were received in the given referral.
        """
        return self.filter(
            referral=referral
        )

    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user 
        """
        return self.filter(
            sender=user
        )

    def inbox_for(self, user, referral):
        """
        Returns all 'new' messages for a pair (user,referral).
        Note that read of messages is marked independently for each user.
        """
        return self.exclude(
            topic__referral=referral,
            readers=user,
            messageread__read_at__isnull=False
        )

class MessageRead(models.Model):
    """
    Each message can be read by each user related to a referral. Thus, this class
    encapsulates all the times at when each user of the referral read the message.
    """
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    user = models.ForeignKey(User)
    message = models.ForeignKey('Message', null=True, blank=True, verbose_name=_("Read status"))


class Message(models.Model):
    """
    A private message in the context of a given referral. Messages are grouped into "topics", and
    topics are related to referrals.
    @see Topic
    """
    topic = models.ForeignKey('MessageTopic', related_name='messages', verbose_name=_('Message topic'))
    body = models.TextField(_("Body"))
    sender = models.ForeignKey(User, related_name='sent_messages', verbose_name=_("Sender"))
    parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True, verbose_name=_("Parent message"))
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    replied_at = models.DateTimeField(_("replied at"), null=True, blank=True)
    sender_deleted_at = models.DateTimeField(_("Sender deleted at"), null=True, blank=True)
    readers = models.ManyToManyField(User, through='MessageRead', related_name="read_messages")
    
    objects = MessageManager()
    
    def __unicode__(self):
        returnValue = ""
        try:
            returnValue=self.topic.subject
        except MessageTopic.DoesNotExist:
            returnValue=""
        return returnValue
            
    def get_absolute_url(self):
        return ('messages_detail', [self.id])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.sent_at = datetime.datetime.now()
        super(Message, self).save(force_insert, force_update) 
   

    def mark_read(self, user):
        """
        method used to mark message as read by a given user
        """
        if user not in self.readers.all():
            message_read = MessageRead()
            message_read.user = user
            message_read.read_at = datetime.datetime.now()
            message_read.message = self
            message_read.save()

    class Meta:
        ordering = ['sent_at']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        get_latest_by = 'sent_at'

class MessageTopic(models.Model):
    """
    A message topic aggregates all the messages in topics. Message topics can be created
    only in a referral context. One message belongs only to one topic.
    """
    subject = models.CharField(_("Subject"), max_length=250, null=True, blank=True)
    referral = models.ForeignKey(Referral, related_name='topics', null=True, blank=True, verbose_name=_("Referral"))
    event = models.ForeignKey(ScheduleOccurrence, null=True, blank=True)
    online_users = models.ManyToManyField(User)
   
    def __unicode__(self):
        return self.subject
    
    class Meta:
        get_latest_by = 'messages__sent_at'

def inbox_count_for(user, referral):
    """
    returns the number of unread messages for the given user in the given referral
    but does not mark them seen
    """
    return Message.objects.inbox_for(user,referral).count()

# fallback for email notification if django-notification could not be found
#if "notification" not in settings.INSTALLED_APPS:
#    from gestorpsi.online_messages.utils import new_message_email
#    signals.post_save.connect(new_message_email, sender=Message)
