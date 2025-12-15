import os
import sys

# Ensure the project directory is on the path
CURRENT_DIR = os.path.dirname(__file__)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)


from base.wsgi import application  # noqa: E402


