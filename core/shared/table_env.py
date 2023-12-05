from pyflink.table import TableEnvironment, EnvironmentSettings
from pyflink.common import Configuration
from core.shared.logger import LoggerSingleton


class TableEnvironmentSingleton:
    def __init__(self):
        self._table_env = None
        self._logger = LoggerSingleton()

    def get_instance(
        self,
        mode: str = "batch",
        opts: Configuration = None,
    ) -> TableEnvironment:
        """
        Get or initialize the TableEnvironment instance.

        Returns:
            TableEnvironment
        """
        if self._table_env is None:
            env_settings = (
                EnvironmentSettings.new_instance().in_streaming_mode()
                if mode == "stream"
                else EnvironmentSettings.new_instance().in_batch_mode()
            )

            if opts is not None:
                env_settings = env_settings.with_configuration(opts)

            self._table_env = TableEnvironment.create(
                environment_settings=env_settings.build()
            )
        return self._table_env
