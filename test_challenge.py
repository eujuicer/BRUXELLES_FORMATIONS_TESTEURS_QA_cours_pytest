"""
Challenge final — process_refund (voir J3_exercices_eleves.md).

Lisez la spécification (énoncé + docstring de process_refund) et écrivez une
suite de tests pertinente et complète.

À VOUS de décider ce dont vous avez besoin : assertions, gestion des cas
interdits, jeux de données, préparation réutilisable, isolation des dépendances…
Rien ne vous est imposé ni suggéré ici : ces choix font partie de l'exercice.

Lancez : pytest test_challenge.py -v
"""

# À vous.
import pytest

from booking import process_refund
from payment import PaymentError


def test_process_refund_success(refund_ok, email_service):
    order = {
        "status": "confirmed",
        "total_cents": 7000,
        "transaction_id": "tx_1",
        "user_email": "leslie@test.com",
    }
    result = process_refund(order, refund_ok, email_service, hours_before_event=72)
    assert result["status"] == "refunded"
    assert result["amount_cents"] == 7000


def test_process_refund_failed(refund_not_ok, email_service):
    order = {
        "status": "confirmed",
        "total_cents": 7000,
        "transaction_id": "tx_1",
        "user_email": "leslie@test.com",
    }
    with pytest.raises(PaymentError):
        process_refund(order, refund_not_ok, email_service, hours_before_event=72)
    email_service.send.assert_not_called()


def test_process_refund_raises_when_order_not_confirmed(refund_ok, email_service):
    order = {
        "status": "pending",
        "total_cents": 7000,
        "transaction_id": "tx_1",
        "user_email": "leslie@test.com",
    }
    with pytest.raises(ValueError):
        process_refund(order, refund_ok, email_service, hours_before_event=72)
    refund_ok.refund.assert_not_called()
    email_service.send.assert_not_called()

def test_process_refund_raises_when_too_late(refund_ok, email_service):
    order = {
        "status": "confirmed",
        "total_cents": 7000,
        "transaction_id": "tx_1",
        "user_email": "leslie"
    }
    with pytest.raises(ValueError):
        process_refund(order, refund_ok, email_service, hours_before_event=47)
    refund_ok.refund.assert_not_called()
    email_service.send.assert_not_called()


def test_process_refund_allowed_at_48h(refund_ok, email_service):
    order = {
        "status": "confirmed",
        "total_cents": 7000,
        "transaction_id": "tx_1",
        "user_email": "leslie@test.com",
    }
    result = process_refund(order, refund_ok, email_service, hours_before_event=48)
    assert result["status"] == "refunded"
    assert result["amount_cents"] == 7000