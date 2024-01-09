FROM docker.io/golebtom/pyflink-conda:v0.2

ARG SCRIPT_PATH

ADD --chown=flink:flink core /opt/flink/usrlib/core
ADD --chown=flink:flink $SCRIPT_PATH /opt/flink/usrlib/pyflink_job.py

RUN mkdir /opt/flink/plugins/hadoop-s3
RUN mkdir /opt/flink/plugins/presto-s3
RUN cp /opt/flink/opt/flink-s3-fs-hadoop-1.18.0.jar  /opt/flink/plugins/hadoop-s3/flink-s3-fs-hadoop-1.18.0.jar
RUN cp /opt/flink/opt/flink-s3-fs-presto-1.18.0.jar  /opt/flink/plugins/presto-s3/flink-s3-fs-presto-1.18.0.jar
