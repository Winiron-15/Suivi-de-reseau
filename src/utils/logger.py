import logging


def setup_logger(name="network_scanner", level=logging.INFO):
    """
    Configure et retourne un logger personnalisé avec un format lisible.

    Args:
        name (str, optional): Nom du logger. Par défaut "network_scanner".
        level (int, optional): Niveau de log (ex: logging.INFO, logging.DEBUG).
          Par défaut INFO.

    Returns:
        logging.Logger: Instance de logger configurée.
    """
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)

    return logger
