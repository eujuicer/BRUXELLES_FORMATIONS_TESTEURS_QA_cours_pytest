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
from unittest.mock import Mock
from booking import create_order



# À vous d'écrire le cas nominal puis de travailler les fixtures.

def test_create_order_nominal(active_user, event, payment_ok, email_service):
    items = [{"category": "standard", "quantity": 2}]
    order = create_order(event, items, active_user, payment_ok, email_service)
    assert order["status"] == "confirmed"
    assert order["total_cents"] == 7000
    assert order["tickets"] == 2
    assert order["user_email"] == "leslie@test.com"
    assert order["transaction_id"] == "tx_1"
