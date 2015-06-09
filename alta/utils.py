import logging

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def a_logger(name, level="WARNING", filename=None, mode="a"):
    log_format = '%(asctime)s|%(levelname)-8s|%(name)s |%(message)s'
    log_datefmt = '%Y-%m-%d %H:%M:%S'
    logger = logging.getLogger(name)
    if not isinstance(level, int):
        try:
            level = getattr(logging, level)
        except AttributeError:
            raise ValueError("unsupported literal log level: %s" % level)
        logger.setLevel(level)
    if filename:
        handler = logging.FileHandler(filename, mode=mode)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format, datefmt=log_datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
