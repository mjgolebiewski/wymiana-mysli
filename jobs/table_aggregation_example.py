from core.shared.table_env import TableEnvironmentSingleton
from pyflink.table import Schema, DataTypes, TableDescriptor
import pyflink.table.expressions as fnc
from pyflink.table.window import Tumble


def main():
    t_env = TableEnvironmentSingleton().get_instance(
        mode="stream",
        opts={
            "log.level": "DEBUG",
            # "python.executable": "/home/mjg/miniconda3/envs/pyflink/bin/python",
            # "pipeline.jars": "file:///home/mjg/dev/pyflink-playground/jars/flink-sql-connector-kafka-3.0.2-1.18.jar",
        },
    )

    # Define intervals for the tumbling window
    interval = fnc.lit(30).seconds

    # Define your Kafka properties
    kafka_address = "http://my-cluster-kafka-plain-bootstrap.kafka:9092"
    # kafka_address = "http://192.168.5.203:9092"

    # Define the table schema
    schema = (
        Schema.new_builder()
        .column("entity_id", DataTypes.STRING())
        .column("state", DataTypes.STRING())
        .column(
            "attributes",
            DataTypes.ROW(
                [
                    DataTypes.FIELD("state_class", DataTypes.STRING()),
                    DataTypes.FIELD("last_reset", DataTypes.STRING()),
                    DataTypes.FIELD("unit_of_measurement", DataTypes.STRING()),
                    DataTypes.FIELD("device_class", DataTypes.STRING()),
                    DataTypes.FIELD("friendly_name", DataTypes.STRING()),
                ],
                nullable=True,
            ),
        )
        .column("last_changed", DataTypes.STRING())
        .column("last_updated", DataTypes.STRING())
        .column(
            "context",
            DataTypes.ROW(
                [
                    DataTypes.FIELD("id", DataTypes.STRING()),
                    DataTypes.FIELD("parent_id", DataTypes.STRING()),
                    DataTypes.FIELD("user_id", DataTypes.STRING()),
                ],
                nullable=True,
            ),
        )
        .column_by_expression(
            "rowtime",
            fnc.to_timestamp(
                fnc.col("last_updated"),
                "yyyy-MM-dd'T'HH:mm:ss.SSSSSS+00:00",
            ),
        )
        .watermark("rowtime", fnc.col("rowtime") - fnc.lit(5).seconds)
        .build()
    )

    t_env.create_temporary_table(
        "kafka_source",
        TableDescriptor.for_connector("kafka")
        .schema(schema)
        .option("properties.bootstrap.servers", kafka_address)
        .option("properties.group.id", "kafka-home-assistant")
        .option("topic", "home_assistant_vpm")
        .option("scan.startup.mode", "earliest-offset")
        .option("value.format", "json")
        .build(),
    )

    table = t_env.from_path("kafka_source")
    w = Tumble.over(interval).on(fnc.col("rowtime")).alias("window")
    table = (
        table.where(
            fnc.col("entity_id")
            == "sensor.power_load_fronius_power_flow_0_192_168_0_181"
        )
        .window(w)
        .group_by(
            fnc.col("entity_id"),
            fnc.col("window"),
            fnc.col("attributes").unit_of_measurement.alias("unit_of_measurement"),
        )
        .select(
            fnc.col("entity_id"),
            fnc.col("unit_of_measurement"),
            fnc.col("state").try_cast(DataTypes.DOUBLE()).avg.alias("avg_state"),
            fnc.col("window").start.alias("window_start"),
            fnc.col("window").end.alias("window_end"),
        )
    )

    schema_out = (
        Schema.new_builder()
        .column("entity_id", DataTypes.STRING())
        .column("unit_of_measurement", DataTypes.STRING())
        .column("avg_state", DataTypes.DOUBLE())
        .column("window_start", DataTypes.TIMESTAMP(3))
        .column("window_end", DataTypes.TIMESTAMP(3))
        .build()
    )

    t_env.create_temporary_table(
        "kafka_sink",
        TableDescriptor.for_connector("kafka")
        .schema(schema_out)
        .option("properties.bootstrap.servers", kafka_address)
        .option("topic", "kafka-sink-topic")
        .option("value.format", "json")
        .build(),
    )

    table.execute_insert("kafka_sink")


if __name__ == "__main__":
    main()
