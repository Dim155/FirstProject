import pytest

from hw1.main.app import create_app, db
from hw1.main.models import Client, Parking


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "parking: mark tests related to parking functionality.",
    )


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    return app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.drop_all()


@pytest.fixture(scope="function")
def sample_data(db_session):
    client = Client(name="Иван", surname="Иванов", car_number="A123BC")
    parking = Parking(
        address="ул. Ленина, д. 1", count_places=10, count_available_places=10
    )
    db_session.add(client)
    db_session.add(parking)
    db_session.commit()
    yield client, parking
    db_session.delete(client)
    db_session.delete(parking)
    db_session.commit()
