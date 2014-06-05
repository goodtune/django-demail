# This file mainly exists to allow python setup.py test to work.

import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_app.settings'

test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

from django.test.utils import get_runner
from django.conf import settings


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['demail'])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
