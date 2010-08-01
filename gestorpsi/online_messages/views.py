import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop
from django.core.urlresolvers import reverse
from django.conf import settings

from gestorpsi.online_messages.models import Message, MessageTopic
from gestorpsi.online_messages.forms import ComposeForm
from gestorpsi.online_messages.utils import format_quote
from gestorpsi.schedule.models import ScheduleOccurrence
from gestorpsi.referral.models import Referral
from gestorpsi.client.models import Client
from gestorpsi.util.decorators import permission_required_with_403
from gestorpsi.client.views import  _access_check_referral_write, _access_check

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

@permission_required_with_403('online_messages.online_messages_read')
def client_messages(request, object_id, referral=None, template_name='messages/messages_user.html'):
    """
    Displays a list of received messages for the given client
    Optional Arguments:
        ``template_name``: name of the template to use.
    """
    message_list = []
    referrals = []

    object = Client.objects.get(pk=object_id, person__organization=request.user.get_profile().org_active)
 
    referrals = Referral.objects.filter(client=object, service__organization=request.user.get_profile().org_active)
 
    for referral in referrals:
        message_list += Message.objects.inbox_for(request.user, referral)

    return render_to_response(template_name, {
        'message_list': message_list,
        'referrals': referrals,
        'messages_user': object,
    }, context_instance=RequestContext(request))
client_messages = login_required(client_messages)

@permission_required_with_403('online_messages.online_messages_read')
def user_messages(request, referral=None, template_name='messages/messages_referral.html'):
    """
    Displays a list of received messages for the current user in the given
    referrals.
    Optional Arguments:
        ``template_name``: name of the template to use.
    """
    if referral is not None:
        message_list = Message.objects.inbox_for(request.user, referral)
        referrals = [referral]
        form = ComposeForm(referral=referral)
    else:
        template_name="messages/messages_user.html"
        message_list = []
        referrals = []

        import logging
        if request.user.profile.person.is_client():
            referrals = Referral.objects.filter(client=request.user.profile.person.client)
        elif request.user.profile.person.is_careprofessional():
            referrals = Referral.objects.filter(professional=request.user.profile.person.careprofessional)
            logging.debug("is care professional")
        else:
            logging.debug("nothing!")

        for referral in referrals:
            message_list += Message.objects.inbox_for(request.user, referral)


    return render_to_response(template_name, {
        'message_list': message_list,
        'referrals': referrals,
    }, context_instance=RequestContext(request))
user_messages = login_required(user_messages)

def _referral_messages(request, referral_id, object_id, template_name="messages/messages_referral.html"):
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    client_id = object_id
    referral = Referral.objects.get(pk=referral_id, service__organization=request.user.get_profile().org_active)

    if not request.user.get_profile().person.is_client():
        # check if professional can read it
        if not _access_check(request, object) and not _access_check_referral_write(request, referral) or object.is_company():
            return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

        if not referral.topics.all():
            return HttpResponseRedirect('/client/%s/referral/%s/messages/newtopic' % (object.id, referral.id))
    #topics = MessageTopic.objects.filter(referral=referral, referral__service__organization=request.user.get_profile().org_active).order_by('messages__sent_at').reverse().distinct()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@permission_required_with_403('online_messages.online_messages_list')
def referral_messages(request, referral_id, object_id):
    return _referral_messages(request, referral_id, object_id, "messages/messages_referral.html")

def _topic_messages(request, referral_id, topic_id, object_id, template_name="messages/messages_topic.html"):
    client_id = object_id

    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    referral = Referral.objects.get(pk=referral_id, service__organization=request.user.get_profile().org_active)

    if not _access_check(request, object) and not _access_check_referral_write(request, referral) or object.is_company():
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    messagetopic = MessageTopic.objects.get(pk=topic_id)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@permission_required_with_403('online_messages.online_messages_list')
def topic_messages(request, referral_id, topic_id, object_id, template_name="messages/messages_topic.html"):
    return _topic_messages(request, referral_id, topic_id, object_id, "messages/messages_topic.html")

def _chat_messages_history(request, object_id, scheduleoccurrence_id, referral_id, redirect_to):
    client_id = object_id

    from django.shortcuts import redirect
    return redirect(redirect_to or "/client/%s/referral/%s/messages/topic/%s" % (client_id, referral_id, messagetopic.id) )

@permission_required_with_403('online_messages.online_messages_read')
def chat_messages_history(request, object_id, scheduleoccurrence_id, referral_id):
    scheduleoccurrence = ScheduleOccurrence.objects.get(pk=scheduleoccurrence_id)

    if scheduleoccurrence.messagetopic_set.count() > 0:
        messagetopic = scheduleoccurrence.messagetopic_set.all()[0]

    return _chat_messages_history(request, object_id, scheduleoccurrence_id, referral_id, "/client/%s/referral/%s/messages/topic/%s" % (object_id, referral_id, messagetopic.id))

def _new_topic_message(request, referral_id, topic_id, object_id, redirect_to=None ):

    client_id = object_id
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    referral = Referral.objects.get(pk=referral_id, service__organization=request.user.get_profile().org_active)

    if not _access_check_referral_write(request, referral) or object.is_company():
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    messagetopic = MessageTopic.objects.get(pk=topic_id)
    if request.POST.get('message'):
        from datetime import datetime
        message = Message()
        message.sender = request.user
        message.sent_at = datetime.now
        message.body = request.POST['message']
        message.topic=messagetopic
        message.save()

        from django.shortcuts import redirect
        return redirect(redirect_to or "/client/%s/referral/%s/messages/topic/%s" % (client_id, referral_id, topic_id))
    else:
        return HttpResponseRedirect(redirect_to or '/client/%s/referral/%s/messages/topic/%s' % (object.id, referral.id, topic_id))

@permission_required_with_403('online_messages.online_messages_write')
def new_topic_message(request, referral_id, topic_id, object_id):
    return _new_topic_message(request, referral_id, topic_id, object_id)

@permission_required_with_403('online_messages_topic.online_messages_topic_write')
def new_message_topic(request, referral_id, object_id, template_name="messages/messages_referral.html"):
    client_id = object_id
    referral = Referral.objects.get(pk=referral_id, service__organization=request.user.get_profile().org_active)
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)

    if not _access_check_referral_write(request, referral) or object.is_company():
        return render_to_response('403.html', {'object': _("Oops! You don't have access for this service!"), }, context_instance=RequestContext(request))

    if not request.POST:
        return render_to_response('messages/messages_newtopic.html', locals(), context_instance=RequestContext(request))

    else:
        messagetopic = MessageTopic()
        messagetopic.referral = referral
        messagetopic.subject = request.POST['topic']
        if request.POST.get('topic'):
            messagetopic.save()
            request.user.message_set.create(message=_('Message topic created successfully'))
            return HttpResponseRedirect('/client/%s/referral/%s/messages/topic/%s' % (client_id, referral.id, messagetopic.id))
        else:
            return HttpResponseRedirect('/client/%s/referral/%s/messages/' % (object.id, referral.id))

def _occurrence_chat(request, object_id, scheduleoccurrence_id, template_name="messages/messages_chat.html"):
    client_id = object_id
    object = get_object_or_404(Client, pk=object_id, person__organization=request.user.get_profile().org_active)
    scheduleoccurrence = ScheduleOccurrence.objects.get(pk=scheduleoccurrence_id)

    if scheduleoccurrence.messagetopic_set.count() == 0:
        messagetopic = MessageTopic()
        messagetopic.subject = "Chat - "
        messagetopic.referral = scheduleoccurrence.event.referral
        messagetopic.event = scheduleoccurrence
        messagetopic.save()
    else:
        messagetopic = scheduleoccurrence.messagetopic_set.all()[0]

    messagetopic.online_users.add(request.user)


    return render_to_response(template_name, {
        'messagetopic': messagetopic,
        'scheduleoccurrence_id': scheduleoccurrence_id,
        'client_id' : client_id,
        'object' : object,
        'referral' : scheduleoccurrence.event.referral,
    }, context_instance=RequestContext(request))

@permission_required_with_403('online_messages.online_messages_write')
def occurrence_chat(request, object_id, scheduleoccurrence_id):
    return _occurrence_chat(request, object_id, scheduleoccurrence_id, 'messages/messages_chat.html')

def _chat_message(request, object_id, messagetopic_id):
    """
    This method is used to allow a user to chat. It is requested using AJAX
    and is used to insert a new message in the current topic.
    """
    messagetopic = MessageTopic.objects.get(pk=messagetopic_id)
    message = Message()
    message.sender = request.user

    message.body = request.POST['messagebody']
    message.topic = messagetopic
    message.save()

    from django.http import HttpResponse
    return HttpResponse("ok")

@permission_required_with_403('online_messages.online_messages_write')
def chat_message(request, object_id, messagetopic_id):
    return _chat_message(request, object_id, messagetopic_id)

def _update_chat_message(request, object_id, messagetopic_id, lastmessage_id):
    """
    This method is used to recover new messages of a chat session. It is requested using AJAX
    and is used to recover messages sent by all chat participants. 
    """
    messagetopic = MessageTopic.objects.get(pk=messagetopic_id)
    messages = Message.objects.filter(topic=messagetopic).filter(pk__gt=int(lastmessage_id))

    return render_to_response("messages/chat_update.html", locals(), context_instance=RequestContext(request))

@permission_required_with_403('online_messages.online_messages_read')
def update_chat_message(request, object_id, messagetopic_id, lastmessage_id):
    return _update_chat_message(request, object_id, messagetopic_id, lastmessage_id)

def _exit_chat(request, object_id, messagetopic_id, redirect_to = None):
    """
    This method is used to allow a user to exit a chat session. The user is marked "offline" when she
    exits the chat session.
    """
    messagetopic = MessageTopic.objects.get(pk=messagetopic_id)
    messagetopic.online_users.remove(request.user)

    from django.shortcuts import redirect
    return redirect(redirect_to or "/client/"+object_id+"/referral/"+str(messagetopic.referral.id))

@permission_required_with_403('online_messages.online_messages_read')
def exit_chat(request, object_id, messagetopic_id):
    return _exit_chat(request, object_id, messagetopic_id)

@permission_required_with_403('online_messages.online_messages_read')
def outbox(request, template_name='messages/outbox.html'):
    """
    Displays a list of sent messages by the current user.
    Optional arguments:
        ``template_name``: name of the template to use.
    """
    message_list = Message.objects.outbox_for(request.user)
    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))
outbox = login_required(outbox)

@permission_required_with_403('online_messages.online_messages_read')
def trash(request, template_name='messages/trash.html'):
    """
    Displays a list of deleted messages. 
    Optional arguments:
        ``template_name``: name of the template to use
    Hint: A Cron-Job could periodicly clean up old messages, which are deleted
    by sender and recipient.
    """
    message_list = Message.objects.trash_for(request.user)
    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))
trash = login_required(trash)

@permission_required_with_403('online_messages.online_messages_write')
def compose(request, recipient=None, form_class=ComposeForm,
        template_name='messages/compose.html', success_url=None, recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user)
            request.user.message_set.create(
                message=_(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            if request.GET.has_key('next'):
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
        # recover this user services
        user = request.user
        profile = user.get_profile()
        person = profile.person
        
        if recipient is not None:
            recipients = [u for u in User.objects.filter(username__in=[r.strip() for r in recipient.split('+')])]
            form.fields['recipient'].initial = recipients
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))
compose = login_required(compose)

@permission_required_with_403('online_messages.online_messages_write')
def reply(request, message_id, form_class=ComposeForm,
        template_name='messages/compose.html', success_url=None, recipient_filter=None):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote.
    """
    parent = get_object_or_404(Message, id=message_id)
    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user, parent_msg=parent)
            request.user.message_set.create(
                message=_(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class({
            'body': _(u"%(sender)s wrote:\n%(body)s") % {
                'sender': parent.sender, 
                'body': format_quote(parent.body)
                }, 
            'subject': _(u"Re: %(subject)s") % {'subject': parent.subject},
            'recipient': [parent.sender,]
            })
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))
reply = login_required(reply)

#@permission_required_with_403('online_messages.online_messages_write')
#def delete(request, message_id, success_url=None):
#    """
#    Marks a message as deleted by sender or recipient. The message is not
#    really removed from the database, because two users must delete a message
#    before it's save to remove it completely.
#    A cron-job should prune the database and remove old messages which are
#    deleted by both users.
#    As a side effect, this makes it easy to implement a trash with undelete.
#
#    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
#    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
#    """
#    user = request.user
#    now = datetime.datetime.now()
#    message = get_object_or_404(Message, id=message_id)
#    deleted = False
#    if success_url is None:
#        success_url = reverse('messages_inbox')
#    if request.GET.has_key('next'):
#        success_url = request.GET['next']
#    if message.sender == user:
#        message.sender_deleted_at = now
#        deleted = True
#    if message.recipient == user:
#        message.recipient_deleted_at = now
#        deleted = True
#    if deleted:
#        message.save()
#        user.message_set.create(message=_(u"Message successfully deleted."))
#        if notification:
#            notification.send([user], "messages_deleted", {'message': message,})
#        return HttpResponseRedirect(success_url)
#    raise Http404
#delete = login_required(delete)

@permission_required_with_403('online_messages.online_messages_write')
def undelete(request, message_id, success_url=None):
    """
    Recovers a message from trash. This is achieved by removing the
    ``(sender|recipient)_deleted_at`` from the model.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    undeleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if request.GET.has_key('next'):
        success_url = request.GET['next']
    if message.sender == user:
        message.sender_deleted_at = None
        undeleted = True
    if message.recipient == user:
        message.recipient_deleted_at = None
        undeleted = True
    if undeleted:
        message.save()
        user.message_set.create(message=_(u"Message successfully recovered."))
        if notification:
            notification.send([user], "messages_recovered", {'message': message,})
        return HttpResponseRedirect(success_url)
    raise Http404
undelete = login_required(undelete)

@permission_required_with_403('online_messages.online_messages_read')
def view(request, message_id, template_name='messages/view.html'):
    """
    Shows a single message.``message_id`` argument is required.
    The user is only allowed to see the message, if he is either 
    the sender or the recipient. If the user is not allowed a 404
    is raised. 
    If the user is the recipient and the message is unread 
    ``read_at`` is set to the current datetime.
    """
    user = request.user
    now = datetime.datetime.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.recipient != user):
        raise Http404
    if message.read_at is None and message.recipient == user:
        message.read_at = now
        message.save()
    return render_to_response(template_name, {
        'message': message,
    }, context_instance=RequestContext(request))
view = login_required(view)
