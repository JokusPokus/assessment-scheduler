# coding=utf-8
import logging

from settings import BASE_DIR

TESTING = True

logging.disable(logging.INFO)
logging.disable(logging.WARNING)


MEDIAFILES_LOCATION = "test-media"
MEDIA_URL = "/test-media/"
MEDIA_ROOT = BASE_DIR + "/" + MEDIAFILES_LOCATION
