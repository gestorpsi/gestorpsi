import locale

def number_format(num):
    return float(num)/100

class RetornoBradescoProcessor:
    """
    Classe especifica para processamento de arquivos de retorno do Bradesco.
    """

    def process_file(self, arquivo_retorno):
        import logging
        from gestorpsi.gcm.models.invoice import *
        import datetime
        #logging.debug(arquivo_retorno.read())
        conteudo = arquivo_retorno.read().splitlines()
        for linha in conteudo[1:-1]:
            documento = int(linha[126:145])
            valor = float(linha[152:165])
            data_pagamento = datetime.datetime.strptime(linha[110:116], "%d%m%y")
            data_credito = linha[295:301]

	    if documento > 100000000:
		      invoice_id = documento - 400000000
	    else:
		      invoice_id = documento


#            invoice_id = documento - 400000000
#            invoice_id = documento - 20000000
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
            #invoice.status = 'pago_boleto'
            #invoice.bank_payed = 'bradesco'
            if valor/100 < float(invoice.ammount):
                invoice.discount = str(valor/100 - float(invoice.ammount))
            else:
                invoice.date_payed = data_pagamento  
            invoice.ammount = valor/100 # valor vem em centavos
            invoice.save()
        except Invoice.DoesNotExist:
            pass

#            logging.debug(int(linha[126:146]))
#            logging.debug(linha[152:165])
#            logging.debug(linha[110:116])
#            logging.debug(linha[295:301])


class RetornoItauProcessor:
    """
    Classe especifica para processamento de arquivos de retorno do banco Itau.
    """

    def process_file(self, arquivo_retorno):
        import logging
        from lecto.subscriptions.models import *
        import datetime
        #logging.debug(arquivo_retorno.read())
        conteudo = arquivo_retorno.read().splitlines()
        for linha in conteudo[1:-1]:
            documento = int(linha[85:93])
            valor = float(linha[152:165])
            data_pagamento = datetime.datetime.strptime(linha[110:116], "%d%m%y")
            data_credito = linha[295:301]

	    if documento > 100000000:
		invoice_id = documento - 400000000
	    else :
		invoice_id = documento


#            invoice_id = documento - 20000000
            try:
                invoice = Invoice.objects.get(pk=invoice_id)
                invoice.payment_date = data_pagamento
                invoice.status = 'pago_boleto'
		invoice.banco_pago = 'itau'
		invoice.value = valor/100
                invoice.save()
            except Invoice.DoesNotExist:
                pass


