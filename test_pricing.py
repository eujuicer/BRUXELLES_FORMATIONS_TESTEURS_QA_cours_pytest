"""
Exercices Bloc 1 & 3 — voir J3_exercices_eleves.md.
Lancez : pytest test_pricing.py -v
"""
import pytest
from pytest import raises
from booking import MAX_TICKETS_PER_ORDER

from booking import ticket_price, line_total, apply_promo, order_total

# À vous d'écrire les tests.


def test_ticket_price():
    assert ticket_price("early_bird") == 2495
    assert ticket_price("standard") == 3500
    assert ticket_price("vip") == 7500

def test_line_total():
    assert line_total("early_bird", 1) == 2495
    assert line_total("standard", 2) == 7000
    assert line_total("vip", 4) == 30000

def test_ticket_price_cat_error():
    with pytest.raises(ValueError):
        ticket_price('vipp')

def test_line_total_quant_error0():
    with pytest.raises(ValueError):
        line_total('vip', 0)

def test_line_total_quant_error_minus1():
    with pytest.raises(ValueError):
        line_total('vip', -1)

codes_test = {
    "valide_code": {
        "code": "VALID",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 1
    },
    "invalide": {
        "code": "INVALID",
        "percent_off": 10,
        "active": False,
        "max_uses": 10,
        "used_count": 1
    },
    "max_used": {
        "code": "USED",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 10
    },
    "low_percent": {
        "code": "LOW",
        "percent_off": 0,
        "active": True,
        "max_uses": 10,
        "used_count": 1
    },
    "high_percent": {
        "code": "HIGH",
        "percent_off": 101,
        "active": True,
        "max_uses": 10,
        "used_count": 1
    }
}

def test_apply_promo():
    assert apply_promo(100, None) == 100
    assert apply_promo(100, codes_test["valide_code"]) == 100 - (100 * 10 // 100)

def test_apply_promo_inactive():
    with pytest.raises(ValueError, match=r"(?i).*inactif"):
        apply_promo(100, codes_test["invalide"])

def test_apply_promo_used():
    with pytest.raises(ValueError, match=r"(?i).*épuisé"):
        apply_promo(100, codes_test["max_used"])

def test_apply_promo_low_percent():
    with pytest.raises(ValueError, match=r"(?i).*invalide"):
        apply_promo(100, codes_test["low_percent"])

def test_apply_promo_high_percent():
    with pytest.raises(ValueError, match=r"(?i).*invalide"):
        apply_promo(100, codes_test["high_percent"])

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ATTENTION CE CODE EN BAS N'EST PAS ECRIT PAR MOI (cc Noé)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def test_order_total_ok() :
    i = [
        {
            "category" : "vip",
            "quantity" : 6
        }
    ]
    assert order_total(i, None) == 6*7500

def test_order_total_tropdetickets() :
    i = [
        {
            "category" : "vip",
            "quantity" : 7
        }
    ]
    with raises(ValueError, match=f"Maximum {MAX_TICKETS_PER_ORDER}"):
        order_total(i,None)

def test_order_total_pasassédetiquets() :
    i = [
        {
            "category" : "vip",
            "quantity" : 0
        }
    ]
    with raises( ValueError, match= "contenir au moins un"):
        order_total(i,None)

def test_order_total_ticket_negatif() :
    i = [
        {
            "category" : "vip",
            "quantity" : -5
        }
    ]
    with raises( ValueError, match= "contenir au moins un"):
        order_total(i,None)


#EXO4 

@pytest.mark.parametrize("category, quantity, expected", [ 
    ("early_bird", 1, 2495),
    ("standard", 2, 3500 *2),
    ("vip", 5, 7500 *5),
], ids=["1_early_bird", "2_standard", "5_vip"])
def test_line_total_all(category, quantity,expected):
    assert line_total(category, quantity) == expected 


#CAS order_total avec plusieurs catégories

@pytest.mark.parametrize("items, expected", [
    ([{"category": "vip", "quantity": 1}], 7500),
    ([{"category": "standard", "quantity": 2}, {"category": "vip", "quantity": 1}], 3500 * 2 + 7500),
    ([{"category": "early_bird", "quantity": 3}, {"category": "vip", "quantity": 3}], 2495 * 3 + 7500 * 3),
], ids=["1_vip", "2_standard_1_vip", "3_early_bird_3_vip_total_6"])
def test_order_total_param(items, expected):
    assert order_total(items) == expected


def test_order_total_multi_categories_total_7_refuse():
    items = [{"category": "early_bird", "quantity": 4}, {"category": "vip", "quantity": 3}]
    with pytest.raises(ValueError, match=f"Maximum {MAX_TICKETS_PER_ORDER}"):
        order_total(items)


#CAS ERREUR

@pytest.mark.parametrize("quantity", [0, -1], ids=["quantity_error0", "quantity_error_minus1"])
def test_line_total_quantity_error(quantity):
    with pytest.raises(ValueError):
        line_total("vip", quantity)


#CAS 6billet MAX 

@pytest.mark.parametrize("quantity", [1, 5, 6], ids=["1_min_ok", "5_ok", "6_limite_ok"])
def test_order_total_quantite_ok(quantity):
    assert order_total([{"category": "standard", "quantity": quantity}]) == 3500 * quantity


@pytest.mark.parametrize("quantity, message", [
    (-1, "au moins un"),
    (0, "au moins un"),
    (7, f"Maximum {MAX_TICKETS_PER_ORDER}"),
], ids=["minus1_refuse", "0_refuse", "7_refuse"])
def test_order_total_quantite_refusee(quantity, message):
    with pytest.raises(ValueError, match=message):
        order_total([{"category": "standard", "quantity": quantity}])


