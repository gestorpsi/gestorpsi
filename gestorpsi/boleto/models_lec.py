from django.utils.translation import ugettext_lazy as _
from lecto.places.models import City
from lecto.phonebook.models import Phonebook
from django.db import models
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from lecto.subscriptions.helpers import RetornoBradescoProcessor, RetornoItauProcessor
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes import generic

class SalesPerson(models.Model):

    name = models.CharField(_('SalesPerson:Name'),help_text=_('SalesPerson:NameHelpText'),max_length=255,null=False,blank=False)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_('SalesPerson:User'))
    comission = models.FloatField(_('SalesPeron:Comission'), null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('SalesPerson:SalesPerson')
        verbose_name_plural = _('SalesPerson:SalesPeople')


TYPE_CHOICES = (
    ('normal', _('type:Normal')),
    ('cortesia', _('type:Free')),
    ('permuta', _('type:Reciprocal')),
)

PERIOD_CHOICES = (
    (1, 'Mensal'),
    (2, 'Bimestral'),
    (3, 'Trimestral'),
    (4, 'Quadrimestral'),
    (6, 'Semestral'),
    (12, 'Anual'),
)

STATUS_CHOICES = (
    ('pendente', _('Pendente')),
    ('pago_boleto', _('Pagoboleto')),
    ('pago_cobranca', _('Pagocobranca')),
    ('pago_escritorio', _('Pagoescritorio')),
    ('cancelado', _('Cancelado')),
    ('inadimplente', _('Inadimplente')),
)

BANK_CHOICES = (
    ('bradesco', 'Bradesco'),
    ('itau', 'Itau'),
)

class Subscription(models.Model):

    first_installment_date = models.DateField(_('subscription:InstallmentDate'),help_text=_('subscription:InstallmentDateHelpText'))
    installment_period = models.IntegerField(_('subscription:InstallmentPeriod'),help_text=_('subscription:InstallmentPeriodHelpText'), choices=PERIOD_CHOICES, null=True,blank=True)
    installment_value = models.FloatField(_('subscription:InstallmentValue'),help_text=_('subscription:InstallmentValueHelpText'), null=True,blank=True)
    due_day = models.IntegerField(_('subscription:DueDate'),help_text=_('subscription:DueDateHelpText'), null=True,blank=True)
    sales_person = models.ForeignKey(SalesPerson, help_text=_('subscription:SalesPerson'), null=True,blank=True)
    type = models.CharField(_('subscription:Type'),help_text=_('subscription:TypeHelpText'),max_length=32,null=False,blank=False,choices=TYPE_CHOICES)
    indicator = models.BooleanField(_('subscription:Indicator'), help_text=_('subscription:IndicatorHelpText'),null=False,default=False)
    needsPaymentDocument = models.BooleanField(_('subscription:NeedsPaymentDocument'), help_text=_('subscription:needsPaymentDocumentHelpText'), null=False, default=True)
    bank = models.CharField(_('Banco'), max_length=32, null=True, blank=True, choices=BANK_CHOICES)
    phonebook = models.ForeignKey(Phonebook, help_text=_('subscription:Phonebook'),null=False,blank=False)

    def invoice_months(self):
        try:
            for i in range(1,13):
                if ((i+self.first_installment_date.month+1)-(self.first_installment_date.month+1)) % self.installment_period == 0:
                    if (i+self.first_installment_date.month) > 11:
                        mes = (i+self.first_installment_date.month+1)%13+1
                        if mes==13:
                            mes=1
                    else:
                        mes = (i+self.first_installment_date.month+1) % 13
                    yield(mes)
        except TypeError:
            import logging
            logging.debug("ERROR NO CADASTRO: " + str(self))


    def save(self, force_insert=False, force_update=False):

        if self.id:
            saved_subscription = Subscription.objects.get(pk=self.id)

            if saved_subscription.installment_period != self.installment_period:
    
                from datetime import datetime
                future_invoices = self.invoice_set.filter(Q(due_date__gt=datetime.today) & 
                                    (Q(status='pendente') | Q(status__isnull=True)) )
                future_invoices.delete()

            if saved_subscription.installment_value != self.installment_value:
    
                from datetime import datetime
                future_invoices = self.invoice_set.filter(Q(due_date__gt=datetime.today) & 
                                    (Q(status='pendente') | Q(status__isnull=True)) )
                future_invoices.delete()

        super(Subscription, self).save(force_insert=force_insert, force_update=force_update)

    def __unicode__(self):
        return u'%s - %s - %s' % (unicode(self.phonebook), self.type, self.installment_value)

    class Meta:
        verbose_name = _('subscription:Subscription')
        verbose_name_plural = _('subscription:Subscriptions')
 
class Invoice(models.Model):

    subscription = models.ForeignKey(Subscription, help_text=_('invoice:SubscriptionHelpText'),null=False,blank=False)
    due_date = models.DateField(_('invoice:DueDate'),help_text=_('invoice:DueDateHelpText'))
    value = models.FloatField(_('invoice:Value'),help_text=_('invoice:ValueHelpText'),null=True,blank=True)
    expected_value = models.FloatField(_('Valor esperado'), null=True, blank=True)
    status = models.CharField(_('invoice:Status'),help_text=_('invoice:StatusHelpText'),max_length=100,null=True,blank=True, choices=STATUS_CHOICES)
    payment_date = models.DateField(_('invoice:PaymentDate'), help_text=_('invoice:PaymentDateHelpText'),null=True,blank=True)
    banco_pago = models.CharField(_('Banco pago'), max_length=20, null=True, blank=True, choices=BANK_CHOICES)
    generated_date = models.DateField('Data gerada', null=True, blank=True, auto_now_add=True)
    lote_rps = models.CharField(_("Lote RPS"), blank=True, null=True, max_length=20)
    logs = generic.GenericRelation(LogEntry)
    last_updated = models.DateTimeField(editable=False,auto_now=True,auto_now_add=True)

    def _phonebook(self):
        return self.subscription.phonebook

    def _phonebook_id(self):
        return self.subscription.phonebook.id

    @property
    def modified_date(self):
        modificacoes = self.logs.filter(action_flag=CHANGE).order_by('-id')
        if modificacoes.count() > 0:
            return modificacoes[0].action_time
        else:
            return None

    def __unicode__(self):
        return '%s %s' % (self._phonebook().company_name, self.value)

    class Meta:
        verbose_name = _('invoice:Invoice')
        verbose_name_plural = _('invoice:Invoices')
        unique_together = ('subscription', 'due_date')


class ReturnFile(models.Model):
    date_import = models.DateTimeField(default=datetime.today, verbose_name=_("Data arquivo"))
    arquivo_retorno = models.FileField(upload_to='arquivos_retorno', verbose_name=_("Arquivo"))
    banco = models.CharField(_('Banco'), max_length=20, null=True,blank=True,choices=BANK_CHOICES)
    #numero registros
    #numero linhas
    
    def save(self, force_insert=False, force_update=False):
        if self.banco == 'bradesco':
            bradesco_processor = RetornoBradescoProcessor()
            bradesco_processor.process_file(arquivo_retorno=self.arquivo_retorno.file)
        if self.banco == 'itau':
            itau_processor = RetornoItauProcessor()
            itau_processor.process_file(arquivo_retorno=self.arquivo_retorno.file)

        super(ReturnFile, self).save()
    
    def __unicode__(self):
        return '%s importado %s' % (self.arquivo_retorno.name, self.date_import) 

    class Meta:
        verbose_name = _('returnFile')
        verbose_name_plural = _('returnFiles')

