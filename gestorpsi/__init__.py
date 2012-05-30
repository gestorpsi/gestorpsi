'''import os
import time
from subprocess import call

#recupera o caminho para o arquivo manage.py
MANAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manage.py')

#varre os processos em busca de alguma instancia do django-celery sendo executado pelo meu projeto
saida = os.popen("ps -ef | grep -i 'gestorpsi/manage.py celeryd' | grep -v grep | awk '{print $2}'").read()

#se a saida for vazia, executa o comando para iniciar o django-celery
if len( str(saida) ) == 0:
    time.sleep(5)
    call("python "+MANAGE+" celeryd -E -B -lINFO &", shell=True)'''