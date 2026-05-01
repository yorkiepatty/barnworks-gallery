import logging

from .redaction import redact

logger = logging.getLogger("alphavox")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def safe_info(m: str):
    logger.info(redact(m))


def safe_warn(m: str):
    logger.warning(redact(m))


def safe_error(m: str):
    logger.error(redact(m))

__all__ = ['safe_info', 'safe_warn', 'safe_error']
