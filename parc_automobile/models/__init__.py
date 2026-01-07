# ============================================
# models/__init__.py
# ============================================
"""
Package models - Modèles de données du système.
Contient les classes représentant les entités métier.
"""

from .vehicule import (
    Vehicule,
    Voiture,
    Moto,
    Utilitaire,
    EtatVehicule,
    CategorieVehicule,
    creer_vehicule_depuis_dict
)

from .mission import (
    Mission,
    StatutMission
)

__all__ = [
    'Vehicule',
    'Voiture',
    'Moto',
    'Utilitaire',
    'EtatVehicule',
    'CategorieVehicule',
    'creer_vehicule_depuis_dict',
    'Mission',
    'StatutMission'
]
