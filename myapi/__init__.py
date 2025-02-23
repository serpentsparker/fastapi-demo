import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s in %(module)s.%(funcName)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
