from typing import Literal
from pyflink.table import TableEnvironment, EnvironmentSettings
from pyflink.common import Configuration
from core.shared.logger import LoggerSingleton


class TableEnvironmentSingleton:
    def __init__(self):
        self._table_env = None
        self._logger = LoggerSingleton()

    def get_instance(
        self, mode: str = Literal["batch", "stream"], opts: dict = None
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
                config = Configuration()
                for k, v in opts.items():
                    config.set_string(k, v)
                env_settings = env_settings.with_configuration(config)

            self._table_env = TableEnvironment.create(
                environment_settings=env_settings.build()
            )
        return self._table_env
