"""
Exercices 5 & 6 — voir J3_exercices_eleves.md.
Lancez : pytest test_orders.py -v

Exercice 5 (fixtures) : create_order a besoin d'un utilisateur, d'un événement
et de deux services externes (paiement, e-mail). Les deux faux services sont
fournis ci-dessous, prêts à l'emploi. Pour l'instant, considérez-les comme des
boîtes noires : on comprendra leur fonctionnement au bloc mocks (exercice 6).

Votre travail ici : écrire le cas nominal de create_order, repérer la répétition
du setup, l'extraire en fixtures, en déplacer dans conftest.py, écrire une
fixture avec yield.

Exercice 6 (mocks) : ensuite seulement, concevez la vraie suite des interactions
de create_order avec ses dépendances (voir énoncé).
"""
import pytest

from booking import create_order
from payment import PaymentError


def test_create_order_confirms_the_order(active_user, event, payment_ok, email_service):
    items = [{"category": "standard", "quantity": 2}]
    order = create_order(event, items, active_user, payment_ok, email_service)
    assert order["status"] == "confirmed"
    assert order["total_cents"] == 7000
    assert order["tickets"] == 2
    assert order["user_email"] == "leslie@test.com"
    assert order["transaction_id"] == "tx_1"


def test_create_order_works_with_tracked_event_fixture(active_user, tracked_event, payment_ok, email_service):
    items = [{"category": "standard", "quantity": 2}]
    order = create_order(tracked_event, items, active_user, payment_ok, email_service)
    assert order["status"] == "confirmed"


def test_create_order_calls_payment_and_sends_email(active_user, event, payment_ok, email_service):
    items = [{"category": "standard", "quantity": 2}]

    create_order(event, items, active_user, payment_ok, email_service)

    payment_ok.charge.assert_called_once_with(7000, "tok_123")
    email_service.send.assert_called_once_with(
        "leslie@test.com",
        "Confirmation de votre commande",
        "Votre commande de 2 billet(s) est confirmée. Montant : 7000 centimes.",
    )


def test_create_order_raises_payment_error_and_sends_no_email(active_user, event, payment_refused, email_service):
    items = [{"category": "standard", "quantity": 2}]

    with pytest.raises(PaymentError):
        create_order(event, items, active_user, payment_refused, email_service)

    email_service.send.assert_not_called()


def test_create_order_raises_when_user_is_inactive(inactive_user, event, email_service, payment_ok):
    items = [{"category": "standard", "quantity": 2}]

    with pytest.raises(ValueError):
        create_order(event, items, inactive_user, payment_ok, email_service)

    payment_ok.charge.assert_not_called()
    email_service.send.assert_not_called()

def test_create_order_raises_when_stock_is_insufficient(active_user, email_service, payment_ok):
    event = {"id":1, "title": "Concert", "available": 1}
    items = [{"category": "standard", "quantity": 2}]

    with pytest.raises(ValueError):
        create_order(event, items, active_user, payment_ok, email_service)

    payment_ok.charge.assert_not_called()   
    email_service.send.assert_not_called()
