import logging

def setup_logger(name="network_scanner", level=logging.INFO):
    """Configure un logger formaté pour l'application."""
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)

    return logger
