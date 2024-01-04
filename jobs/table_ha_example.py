from core.shared.table_env import TableEnvironmentSingleton
from pyflink.table import Schema, DataTypes, TableDescriptor
import pyflink.table.expressions as fnc

# , FormatDescriptor


def main():
    t_env = TableEnvironmentSingleton().get_instance(
        mode="stream",
        opts={
            "log.level": "DEBUG",
            # "python.executable": "/home/mjg/miniconda3/envs/pyflink/bin/python",
            # "pipeline.jars": "file:///home/mjg/dev/pyflink-playground/jars/flink-sql-connector-kafka-3.0.2-1.18.jar",
        },
    )

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
        .build()
    )

    kafka_address = "http://192.168.5.205:9092"

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
    table = table.where(
        (fnc.col("entity_id") == "sensor.battery_sim_lg_chem_current_discharging_rate")
        & (fnc.col("state") == "0.0")
    )

    t_env.create_temporary_table(
        "kafka_sink",
        TableDescriptor.for_connector("kafka")
        .schema(schema)
        .option("properties.bootstrap.servers", kafka_address)
        .option("topic", "kafka-sink-topic")
        .option("value.format", "json")
        .build(),
    )

    # # TODO: zapis do minio s3
    # t_env.create_temporary_table(
    #     "minio_sink",
    #     TableDescriptor.for_connector("filesystem")
    #     .format(FormatDescriptor.for_format("parquet").build())
    #     .option("path", "s3://192.168.5.208:9001/flink-sink")
    #     .schema(schema)
    #     .build(),
    # )
    # table.execute_insert("minio_sink")

    # table.execute_insert("kafka_sink")


if __name__ == "__main__":
    main()
