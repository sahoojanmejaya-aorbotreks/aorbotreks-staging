# staging.py
from .settings import *

import os

DEBUG = True  # Keep ON for testing

ALLOWED_HOSTS = [
    "staging.aorbotreks.com",
    "localhost",
    "127.0.0.1",
    "[::1]"  # IPv6 localhost
]

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
