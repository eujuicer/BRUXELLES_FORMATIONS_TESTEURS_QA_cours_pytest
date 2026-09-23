"""
Exercice Bloc 2 — Code hérité (voir énoncé).
Lisez la spécification dans legacy_pricing.py, concevez vos cas, écrivez vos
tests, lancez-les, et diagnostiquez tout écart avec la spécification.
Lancez : pytest test_legacy.py -v
"""
from legacy_pricing import loyalty_discount_percent, price_with_loyalty

# À vous d'écrire les tests
"""
Exercice Bloc 2 — Code hérité.

Lancez : pytest test_legacy.py -v
"""

from legacy_pricing import loyalty_discount_percent, price_with_loyalty


def test_loyalty_discount_percent_low():
    # 0 à 2 commandes -> 0 %
    assert loyalty_discount_percent(0) == 0
    assert loyalty_discount_percent(2) == 0

def test_loyalty_discount_percent_medium():
    # 0 à 2 commandes -> 0 %
    # 3 à 9 commandes -> 5 %
    assert loyalty_discount_percent(3) == 5
    assert loyalty_discount_percent(9) == 5

def test_loyalty_discount_percent_high():
    # 0 à 2 commandes -> 0 %
    # 10 commandes ou plus -> 10 %
    assert loyalty_discount_percent(10) == 10
    assert loyalty_discount_percent(11) == 10


def test_price_with_loyalty_low():
    assert price_with_loyalty(1000, 0) == 1000
    assert price_with_loyalty(1000, 2) == 1000

def test_price_with_loyalty_medium():
    assert price_with_loyalty(1000, 3) == 950
    assert price_with_loyalty(1000, 9) == 950

def test_price_with_loyalty_high():
    assert price_with_loyalty(1000, 10) == 900
    assert price_with_loyalty(1000, 11) == 900