from core.shared.stream_env import StreamExecutionEnvironmentSingleton
from pyflink.common import Types
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.datastream.formats.json import JsonRowDeserializationSchema


def main():
    # Get the TableEnvironment instance
    s_env = StreamExecutionEnvironmentSingleton().get_instance(
        {
            "log.level": "DEBUG",
            "python.executable": "/home/mjg/miniconda3/envs/pyflink/bin/python",
        }
    )
    s_env.add_jars(
        "file:///home/mjg/dev/pyflink-playground/jars/flink-sql-connector-kafka-3.0.2-1.18.jar"
    )

    # Define your Kafka properties
    kafka_properties = {"bootstrap.servers": "localhost:9092", "group.id": "gid"}

    # Define the schema of your Kafka topic
    type_info = Types.ROW([Types.BIG_INT(), Types.INT()])
    schema = JsonRowDeserializationSchema.builder().type_info(type_info).build()

    # Register Kafka source
    kafka_consumer = FlinkKafkaConsumer(
        topics="mock-data",
        deserialization_schema=schema,
        properties=kafka_properties,
    )

    kafka_consumer.set_start_from_earliest()

    s_env.add_source(kafka_consumer).print()
    s_env.execute("KafkaConsumerJob")


if __name__ == "__main__":
    main()
