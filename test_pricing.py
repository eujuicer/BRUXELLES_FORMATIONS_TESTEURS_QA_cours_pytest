"""
Exercices Bloc 1 & 3 — voir J3_exercices_eleves.md.
Lancez : pytest test_pricing.py -v
"""
import pytest
from booking import ticket_price, line_total, apply_promo, order_total

# À vous d'écrire les tests.
def test_ticket_price():
    assert ticket_price("early_bird") == 2495 
    assert ticket_price("standard") == 3500
    assert ticket_price("vip") == 7500

def test_ticket_price_error():
    with pytest.raises(ValueError):
        ticket_price("unknown")


def test_line_total():
    assert line_total("early_bird", 1) == 2495
    assert line_total("standard", 3) == 3500 * 3
    assert line_total("vip", 6) == 7500 * 6

def test_line_total_error():
    with pytest.raises(ValueError, match="La quantité doit être strictement positive"):
        line_total("standard", 0)


def test_apply_promo_none():
    assert apply_promo(1000, None) == 1000

def test_apply_promo_inactive():
    promo_inactive = {
        "code": "PROMO10",
        "percent_off": 10,
        "active": False,
        "max_uses": 10,
        "used_count":0
    }
    with pytest.raises(ValueError, match="Code promo inactif"):
        apply_promo(1000, promo_inactive)

def test_apply_promo_quota():
    promo_quotas = {
        "code": "PROMO10",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 11,
    }
    with pytest.raises(ValueError, match="Code promo épuisé"):
        apply_promo(1000, promo_quotas)

def test_apply_promo_percent_off():
    promo_percent_off = {
        "code": "PROMO10",
        "percent_off": 101,
        "active": True,
        "max_uses": 10,
        "used_count": 0,
    }
    with pytest.raises(ValueError, match="Pourcentage de remise invalide"):
        apply_promo(1000, promo_percent_off)


order_total()

def test_order_total_empty():
    with pytest.raises(
        ValueError,
        match="Une commande doit contenir au moins un billet"):
        order_total([])


def test_order_total_too_many_tickets():
    items = [
        {"category": "standard", "quantity": 7}
    ]

    with pytest.raises(
        ValueError,
        match="Maximum 6 billets par commande"
    ):
        order_total(items)


def test_order_total_max_allowed():
    items = [{"category": "standard", "quantity": 6}]
    assert order_total(items) == 21000


def test_order_total_invalid_quantity():
    items = [
        {"category": "standard", "quantity": 0}
    ]

    with pytest.raises(
        ValueError,
        match="La quantité doit être strictement positive"
    ):
        order_total(items)


def test_order_total_unknown_category():
    items = [{"category": "inconnue", "quantity": 1} ]
    with pytest.raises(ValueError, match="Catégorie de billet inconnue"):
        order_total(items)