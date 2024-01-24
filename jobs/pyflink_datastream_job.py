from core.shared.stream_env import StreamExecutionEnvironmentSingleton
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.datastream.formats.json import (
    JsonRowDeserializationSchema,
    JsonRowSerializationSchema,
)
from pyflink.common import Types


def main():
    # Get the TableEnvironment instance
    s_env = StreamExecutionEnvironmentSingleton().get_instance(
        {
            "log.level": "DEBUG",
        },
    )

    s_env.add_jars("file:///opt/flink/lib/flink-sql-connector-kafka-3.0.2-1.18.jar")
    # s_env.get_checkpoint_config().set_checkpoint_interval(
    #     30000
    # ).set_tolerable_checkpoint_failure_number(2)

    # Define your Kafka properties
    kafka_properties = {
        "bootstrap.servers": "my-cluster-kafka-plain-bootstrap.kafka:9092",
        "group.id": "kafka-home-assistant",
    }

    # Define the type information for the result stream
    type_info = Types.ROW_NAMED(
        ["entity_id", "state", "attributes", "last_changed", "last_updated", "context"],
        [
            Types.STRING(),  # entity_id
            Types.STRING(),  # state
            Types.ROW_NAMED(
                [
                    "state_class",
                    "last_reset",
                    "unit_of_measurement",
                    "device_class",
                    "friendly_name",
                ],
                [
                    Types.STRING(),  # state_class
                    Types.STRING(),  # last_reset
                    Types.STRING(),  # unit_of_measurement
                    Types.STRING(),  # device_class
                    Types.STRING(),  # friendly_name
                ],
            ),  # attributes
            Types.STRING(),  # last_changed
            Types.STRING(),  # last_updated
            Types.ROW_NAMED(
                ["id", "parent_id", "user_id"],
                [
                    Types.STRING(),  # id
                    Types.STRING(),  # parent_id
                    Types.STRING(),  # user_id
                ],
            ),  # context
        ],
    )

    # Define the type information for the result stream
    schema = JsonRowDeserializationSchema.builder().type_info(type_info).build()

    # Register Kafka source
    kafka_consumer = FlinkKafkaConsumer(
        topics="home_assistant_vpm",
        deserialization_schema=schema,
        properties=kafka_properties,
    ).set_start_from_earliest()

    # Add Kafka source to the StreamExecutionEnvironment
    stream_source = s_env.add_source(kafka_consumer)

    # Define the aggregation logic
    result_stream = stream_source.filter(
        lambda x: x["entity_id"] == "switch.shellyplus2pm_b8d61a89efac_switch_1"
        and x["state"] == "on"
    )

    # Define the serialization schema
    schema_sink = JsonRowSerializationSchema.builder().with_type_info(type_info).build()

    # Define the Kafka sink
    kafka_producer = FlinkKafkaProducer(
        topic="kafka-sink-topic-datastream",
        serialization_schema=schema_sink,
        producer_config=kafka_properties,
    )

    # Add the Kafka sink to the result stream
    result_stream.add_sink(kafka_producer)

    s_env.execute("HA Data")


if __name__ == "__main__":
    main()
