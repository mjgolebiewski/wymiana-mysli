from core.shared.table_env import TableEnvironmentSingleton
from pyflink.table import Schema, DataTypes, TableDescriptor
import pyflink.table.expressions as fnc
from pyflink.table.window import Tumble


def main():
    t_env = TableEnvironmentSingleton().get_instance(
        mode="stream",
        opts={
            "log.level": "DEBUG",
            "python.executable": "/home/mjg/miniconda3/envs/pyflink/bin/python",
            "pipeline.jars": "file:///home/mjg/dev/pyflink-playground/jars/flink-sql-connector-kafka-3.0.2-1.18.jar",
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
        .column_by_expression(
            "rowtime",
            fnc.to_timestamp(
                fnc.col("last_updated"), "yyyy-MM-ddTHH:mm:ss.SSSSSS+00:00"
            ),  # "2024-01-03T10:25:07.714169+00:00"
        )
        .watermark("rowtime", fnc.col("rowtime") - fnc.lit(10).seconds)
        .build()
    )

    t_env.create_temporary_table(
        "kafka_source",
        TableDescriptor.for_connector("kafka")
        .schema(schema)
        .option("properties.bootstrap.servers", "http://192.168.5.205:9092")
        .option("properties.group.id", "kafka-home-assistant")
        .option("topic", "home_assistant_vpm")
        .option("scan.startup.mode", "latest-offset")
        .option("value.format", "json")
        .build(),
    )

    table = t_env.from_path("kafka_source")
    w = Tumble.over(fnc.lit(10).seconds).on(fnc.col("rowtime")).alias("window")
    table = (
        table.window(w)
        .group_by(fnc.col("entity_id"), fnc.col("window"))
        .select(
            fnc.col("entity_id"),
            fnc.col("state").try_cast(DataTypes.DOUBLE()).avg.alias("avg_state"),
        )
    )

    schema_out = (
        Schema.new_builder()
        .column("entity_id", DataTypes.STRING())
        .column("avg_state", DataTypes.DOUBLE())
        .build()
    )

    t_env.create_temporary_table(
        "kafka_sink",
        TableDescriptor.for_connector("kafka")
        .schema(schema_out)
        .option("properties.bootstrap.servers", "localhost:29092")
        .option("topic", "kafka-sink-topic")
        .option("value.format", "json")
        .build(),
    )

    table.execute_insert("kafka_sink")


if __name__ == "__main__":
    main()
