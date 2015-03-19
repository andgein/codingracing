__author__ = 'Andrew Gein <andgein@yandex.ru>'

import os


VK_APP_ID = 4828476
VK_APP_SECRET = 'aUTz02DMmzQI6d2kQBfo'
VK_REDIRECT_URL = 'http://127.0.0.1:8000/auth'

LEVENSHTEIN_PENALTY = 5
DELAY_GAME_START = 5  # in seconds

COOKIE_HASH = 'super_s3cr3t_hash_F0R_konturgonki.ru'

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)

MAX_USERS_IN_CONTEST = 4

# VK ids
MANAGERS = [5150346, 5445276, 2473168, 542854]