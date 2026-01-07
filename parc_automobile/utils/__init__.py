# ============================================
# utils/__init__.py
# ============================================
"""
Package utils - Utilitaires du système.
Contient les fonctions et classes transverses.
"""

from .stockage import GestionnaireStockage, StockageException

__all__ = [
    'GestionnaireStockage',
    'StockageException'
]
