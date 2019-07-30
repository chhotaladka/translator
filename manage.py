#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import threading
from importlib import import_module
server = import_module('translator.backend.google-selenium-asyncio.server')
selenium_server = threading.Thread(target=server.main)
selenium_server.setDaemon(True)
selenium_server.start()

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
