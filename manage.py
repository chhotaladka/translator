#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import multiprocessing
from importlib import import_module
server = import_module('translator.backend.google-selenium-asyncio.server')
client = import_module('translator.backend.google-selenium-asyncio.api')
selenium_server = multiprocessing.Process(target=server.main)
selenium_server.daemon = True
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
    selenium_server.terminate()
    selenium_server.join()
