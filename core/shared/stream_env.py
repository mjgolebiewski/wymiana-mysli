from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Configuration
from core.shared.logger import LoggerSingleton


class StreamExecutionEnvironmentSingleton:
    def __init__(self):
        self._stream_env = None
        self._logger = LoggerSingleton()

    def get_instance(self, opts: dict = None) -> StreamExecutionEnvironment:
        """
        Get or initialize the StreamExecutionEnvironment instance.

        Returns:
            StreamExecutionEnvironment
        """
        if self._stream_env is None:
            config = Configuration()
            if opts is not None:
                for k, v in opts.items():
                    config.set_string(k, v)

            self._stream_env = StreamExecutionEnvironment.get_execution_environment(
                configuration=config
            )
        return self._stream_env
