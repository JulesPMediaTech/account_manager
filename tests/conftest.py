'''
As a pytest conftest file, this sets up fixtures for testing the application.
It sets the Python path to include the app directory for imports. (sys.path.insert)

TO RUN TESTS:
pytest tests/
'''




from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from app.OLD_ORIG_server import app  # noqa: E402


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
