# The node were rabbitmq is running.
BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'

# With this setting celeryd kills the worker process for each task.
# Useful if your tasks use much memory.
CELERYD_MAX_TASKS_PER_CHILD = 1

# Specify how many processes are used for celeryd tasks.
CELERYD_CONCURRENCY = 1

# The default logging format is not nice.
CELERYD_LOG_FORMAT = "[%(asctime)s: %(levelname)s/%(processName)s] %(name)s - %(message)s"