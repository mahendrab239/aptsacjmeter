FROM centos:centos7 
RUN yum -y update \
    && yum clean all \
    && yum install -y curl \
    && yum install -y sudo \
    && yum install -y bash 
RUN curl -sL https://rpm.nodesource.com/setup_16.x | sudo bash - 
RUN yum install -y nodejs \
    && npm install -g lighthouse \
    && yum install -y wget \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm \
    && yum -y localinstall google-chrome-stable_current_x86_64.rpm
WORKDIR /report
