FROM docker.io/golebtom/pyflink-conda:v0.2

ARG SCRIPT_PATH

ADD --chown=flink:flink core /opt/flink/usrlib/core
ADD --chown=flink:flink $SCRIPT_PATH /opt/flink/usrlib/pyflink_job.py
