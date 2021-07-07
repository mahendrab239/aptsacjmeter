ARG ELK_VERSION

FROM docker.elastic.co/beats/filebeat:${ELK_VERSION}
COPY filebeat-docker.yml /usr/share/filebeat/filebeat.yml
USER root
RUN chown root:filebeat /usr/share/filebeat/filebeat.yml
USER filebeat
