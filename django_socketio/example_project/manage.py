#!/usr/bin/env python
import sys
import os

from settings import PROJECT_DIR, PROJECT_ROOT

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, "..")))

if __name__ == "__main__":
    settings_module = "%s.settings" % PROJECT_DIR
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
