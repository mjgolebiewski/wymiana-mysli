FROM docker.io/golebtom/pyflink-hello-world:v0.25

ARG SCRIPT_PATH

ADD --chown=flink:flink core /opt/flink/usrlib/core
ADD --chown=flink:flink $SCRIPT_PATH /opt/flink/usrlib/pyflink_job.py
