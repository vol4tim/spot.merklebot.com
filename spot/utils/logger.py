import logging
logging.basicConfig(
    level=logging.INFO,
    filename=f"/logs/spot.log",
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S")

logger = logging.getLogger('spot')
