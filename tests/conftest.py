# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from yolp import YOLP  # NOQA


@pytest.fixture
def yolp(request):
    return YOLP(os.environ.get('YAHOO_APP_ID'))
