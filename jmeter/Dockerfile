# Use Java 8 slim JRE
FROM openjdk:8-jre-slim

MAINTAINER Bharat Goyal<bharat.goyal@publicissapient.com>

# JMeter version
ARG JMETER_VERSION=5.2.1

# Install few utilities
RUN apt-get clean && \
    apt-get update && \
    apt-get -qy install \
                wget \
                tar \
                bash

# Install JMeter
RUN   wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-$JMETER_VERSION.tgz \
      && mkdir -p /opt/jmeter \
	  && tar -zxf apache-jmeter-$JMETER_VERSION.tgz -C /opt/jmeter/ --strip-components=1 \
      && rm -rf apache-jmeter-$JMETER_VERSION.tgz


# Set JMeter Home
ENV JMETER_HOME=/opt/jmeter


# Add JMeter to the Path
ENV PATH $JMETER_HOME/bin:$PATH

EXPOSE 60000
