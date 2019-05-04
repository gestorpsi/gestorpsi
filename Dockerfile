FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /gestorpsi
WORKDIR /gestorpsi
ADD requirements.txt /gestorpsi/
ENV LANG C
RUN pip install -r requirements.txt
ADD gestorpsi/ /gestorpsi/
COPY ./docker/settings.py /gestorpsi/
COPY ./manage.py /