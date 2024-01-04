FROM docker.io/golebtom/pyflink-hello-world:v0.25

ADD --chown=flink:flink core /opt/flink/usrlib/core
ADD --chown=flink:flink jobs/table_aggregation_example.py /opt/flink/usrlib/pyflink_job.py
