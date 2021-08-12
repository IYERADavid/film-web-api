import pytest
from flask_app import app

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    flask_app = app
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
