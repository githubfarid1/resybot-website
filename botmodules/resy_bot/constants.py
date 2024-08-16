from enum import Enum
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)
from settings import RETRY_VALUE

RESY_BASE_URL = "https://api.resy.com"
N_RETRIES = RETRY_VALUE
SECONDS_TO_WAIT_BETWEEN_RETRIES = 0.05

class ResyEndpoints(Enum):
    FIND = "/4/find"
    DETAILS = "/3/details"
    BOOK = "/3/book"
    PASSWORD_AUTH = "/3/auth/password"
    # frd
    USER = "/2/user"
    VENUE = ""