from core.shared.table_env import TableEnvironmentSingleton
from pyflink.table import CsvTableSink, WriteMode, DataTypes
import pyflink.table.expressions as expr
import pandas as pd


def main():
    t_env = TableEnvironmentSingleton().get_instance()
    t_env.get_config().set("execution.target", "local")

    # Define the table schema
    field_names = ["word", "count"]
    field_types = [DataTypes.STRING(), DataTypes.BIGINT()]
    words = [
        ("apple", 1),
        ("orange", 1),
        ("apple", 1),
        ("banana", 1),
        ("orange", 1),
        ("apple", 1),
        ("banana", 1),
        ("apple", 1),
    ]

    # Define the CSV table sink
    csv_table_sink = CsvTableSink(
        field_names=field_names,
        field_types=field_types,
        path="/home/mjg/dev/pyflink-playground/data/output/word_count_table.csv",
        field_delimiter=",",
        write_mode=WriteMode.OVERWRITE,
    )

    # Register the table sink
    t_env.register_table_sink("my_sink", csv_table_sink)

    # Create a pandas DataFrame from the hardcoded data
    df = pd.DataFrame(words, columns=field_names)

    # Define the PyFlink job
    result_table = (
        t_env.from_pandas(df, schema=field_names)
        .group_by(expr.col("word"))
        .select(expr.col("word"), expr.col("count").count.alias("count"))
    )

    # Insert the result into the CSV table sink
    result_table.execute_insert("my_sink").wait()


if __name__ == "__main__":
    main()
