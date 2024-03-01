"""
    Dummy conftest.py for plistparse.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

from types import SimpleNamespace as SimpleNameSpace

import pytest

# Temporary Storage

pytest.tmp = SimpleNameSpace()


@pytest.fixture(autouse=True, scope="class")
def set_tmp_cls():
    pytest.tmp.cls = SimpleNameSpace()


@pytest.fixture(autouse=True, scope="module")
def set_tmp_mod():
    pytest.tmp.mod = SimpleNameSpace()
