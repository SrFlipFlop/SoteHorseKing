FROM ubuntu:latest

RUN apt update && apt install  openssh-server sudo -y

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 test 

RUN  echo 'test:test' | chpasswd

RUN service ssh start

WORKDIR /home/ubuntu

COPY ./config ./config

RUN mkdir ./.ssh/ && cat ./config/id_rsa.pub > ./.ssh/authorized_keys && rm ./config/

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]