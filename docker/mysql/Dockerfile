FROM mariadb:latest

RUN mkdir -p /var/lib/mysql
COPY var/* /var/lib/mysql/

ENV MYSQL_ROOT_PASSWORD root
ENV MYSQL_DATABASE gestorpsi
ENV MYSQL_USER root
ENV MYSQL_PASSWORD root

RUN apt-get update && apt-get -y install vim

EXPOSE 3306

CMD ["mysqld"]