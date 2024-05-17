def create_logging_function(enable_logging: bool):
    def log(x):
        return print(x) if enable_logging else None
    return log
