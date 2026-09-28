"""
conftest.py — fixtures partagées entre plusieurs fichiers de test.

Vide au départ : vous y déplacerez vos fixtures au Bloc 5, quand plusieurs
fichiers auront besoin des mêmes données ou des mêmes mocks.
Pytest découvre ce fichier automatiquement : aucune importation nécessaire.
"""

from unittest.mock import Mock

import pytest


@pytest.fixture
def get_user():
    fixture_user =  {"name": "Leslie", "formation": "QA test"}
    return fixture_user

@pytest.fixture
def get_confirm():
    return {"result": True}

@pytest.fixture
def db(base_donne):
    db = base_donne.open()
    print("Conexion")
    yield db
    print('Deconexion')


@pytest.fixture(scope="session")
def email_mock_service():
    mock_email = Mock()
    mock_email.error.side_effect = ValueError("hehe je suis une erreure")
    mock_email.send.return_value = {"ok": True}
    mock_email.display.return_value = {"ok": True}

    return mock_email


@pytest.fixture
def payment_ok():
    payment = Mock()
    payment.charge.return_value = {"success": True, "transaction_id": "tx_1"}
    return payment

@pytest.fixture
def payment_refused():
    payment = Mock()
    payment.charge.return_value = {"success": False, "transaction_id": None}
    return payment

@pytest.fixture
def email_service():
    return Mock()

@pytest.fixture
def active_user():
    return {"email": "leslie@test.com", "active": True, "payment_token": "tok_123"}

@pytest.fixture
def event():
    return {"id": 1, "title": "Concert", "available": 10}


@pytest.fixture
def tracked_event():
    ev = {"id": 1, "title": "Concert", "available": 10}
    print(f"\n[avant test] stock disponible : {ev['available']}")
    yield ev
    print(f"[après test] stock disponible : {ev['available']}")


@pytest.fixture
def inactive_user():
    return {"email": "leslie@test.com", "active": False, "payment_token": "tok_123"}

@pytest.fixture
def refund_ok():
    payment_gateway = Mock()
    payment_gateway.refund.return_value = {"success": True}
    return payment_gateway

@pytest.fixture
def refund_not_ok():
    payment_gateway = Mock()
    payment_gateway.refund.return_value = {"success": False}
    return payment_gateway
    