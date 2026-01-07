"""
Module de définition des classes de véhicules.
Utilise l'héritage et la POO avancée.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class EtatVehicule(Enum):
    """Énumération des états possibles d'un véhicule."""
    DISPONIBLE = "disponible"
    EN_MISSION = "en_mission"
    EN_MAINTENANCE = "en_maintenance"
    HORS_SERVICE = "hors_service"


class CategorieVehicule(Enum):
    """Énumération des catégories de véhicules."""
    VOITURE = "voiture"
    MOTO = "moto"
    UTILITAIRE = "utilitaire"


class Vehicule:
    """Classe de base pour tous les véhicules du parc."""
    
    def __init__(
        self,
        immatriculation: str,
        marque: str,
        modele: str,
        annee: int,
        kilometrage: float = 0.0,
        cout_acquisition: float = 0.0,
        cout_maintenance: float = 0.0,
        cout_carburant: float = 0.0,
        etat: EtatVehicule = EtatVehicule.DISPONIBLE
    ):
        """
        Initialise un véhicule.
        
        Args:
            immatriculation: Numéro d'immatriculation unique
            marque: Marque du véhicule
            modele: Modèle du véhicule
            annee: Année de mise en circulation
            kilometrage: Kilométrage actuel
            cout_acquisition: Coût d'acquisition du véhicule
            cout_maintenance: Coût de maintenance cumulé
            cout_carburant: Coût de carburant cumulé
            etat: État actuel du véhicule
            
        Raises:
            ValueError: Si les paramètres sont invalides
        """
        self._valider_parametres(immatriculation, annee, kilometrage, cout_acquisition)
        
        self.immatriculation = immatriculation.upper()
        self.marque = marque.title()
        self.modele = modele
        self.annee = annee
        self.kilometrage = kilometrage
        self.cout_acquisition = cout_acquisition
        self.cout_maintenance = cout_maintenance
        self.cout_carburant = cout_carburant
        self.etat = etat if isinstance(etat, EtatVehicule) else EtatVehicule(etat)
        self.date_ajout = datetime.now()
    
    def _valider_parametres(self, immat: str, annee: int, km: float, cout: float):
        """Valide les paramètres du véhicule."""
        if not immat or len(immat.strip()) == 0:
            raise ValueError("L'immatriculation ne peut pas être vide")
        
        annee_actuelle = datetime.now().year
        if annee < 1900 or annee > annee_actuelle + 1:
            raise ValueError(f"Année invalide: {annee}")
        
        if km < 0:
            raise ValueError("Le kilométrage ne peut pas être négatif")
        
        if cout < 0:
            raise ValueError("Le coût ne peut pas être négatif")
    
    @property
    def categorie(self) -> CategorieVehicule:
        """Retourne la catégorie du véhicule."""
        raise NotImplementedError("Doit être implémenté par les sous-classes")
    
    @property
    def age(self) -> int:
        """Calcule l'âge du véhicule en années."""
        return datetime.now().year - self.annee
    
    @property
    def cout_total(self) -> float:
        """Calcule le coût total du véhicule."""
        return self.cout_acquisition + self.cout_maintenance + self.cout_carburant
    
    def ajouter_kilometrage(self, kilometres: float):
        """
        Ajoute des kilomètres au compteur.
        
        Args:
            kilometres: Nombre de kilomètres à ajouter
            
        Raises:
            ValueError: Si les kilomètres sont négatifs
        """
        if kilometres < 0:
            raise ValueError("Les kilomètres ne peuvent pas être négatifs")
        self.kilometrage += kilometres
    
    def changer_etat(self, nouvel_etat: EtatVehicule):
        """Change l'état du véhicule."""
        if not isinstance(nouvel_etat, EtatVehicule):
            nouvel_etat = EtatVehicule(nouvel_etat)
        self.etat = nouvel_etat
    
    def ajouter_cout_maintenance(self, cout: float):
        """Ajoute un coût de maintenance."""
        if cout < 0:
            raise ValueError("Le coût ne peut pas être négatif")
        self.cout_maintenance += cout
    
    def ajouter_cout_carburant(self, cout: float):
        """Ajoute un coût de carburant."""
        if cout < 0:
            raise ValueError("Le coût ne peut pas être négatif")
        self.cout_carburant += cout
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le véhicule en dictionnaire."""
        return {
            'immatriculation': self.immatriculation,
            'marque': self.marque,
            'modele': self.modele,
            'annee': self.annee,
            'kilometrage': self.kilometrage,
            'cout_acquisition': self.cout_acquisition,
            'cout_maintenance': self.cout_maintenance,
            'cout_carburant': self.cout_carburant,
            'etat': self.etat.value,
            'categorie': self.categorie.value,
            'date_ajout': self.date_ajout.isoformat()
        }
    
    def __str__(self) -> str:
        return (f"{self.categorie.value.title()} - {self.marque} {self.modele} "
                f"({self.annee}) - {self.immatriculation} - {self.etat.value}")
    
    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(immatriculation='{self.immatriculation}', "
                f"marque='{self.marque}', modele='{self.modele}')")


class Voiture(Vehicule):
    """Classe représentant une voiture."""
    
    def __init__(
        self,
        immatriculation: str,
        marque: str,
        modele: str,
        annee: int,
        nombre_places: int = 5,
        **kwargs
    ):
        super().__init__(immatriculation, marque, modele, annee, **kwargs)
        if nombre_places < 2 or nombre_places > 9:
            raise ValueError("Nombre de places invalide pour une voiture")
        self.nombre_places = nombre_places
    
    @property
    def categorie(self) -> CategorieVehicule:
        return CategorieVehicule.VOITURE
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['nombre_places'] = self.nombre_places
        return data


class Moto(Vehicule):
    """Classe représentant une moto."""
    
    def __init__(
        self,
        immatriculation: str,
        marque: str,
        modele: str,
        annee: int,
        cylindree: int = 125,
        **kwargs
    ):
        super().__init__(immatriculation, marque, modele, annee, **kwargs)
        if cylindree < 50 or cylindree > 2000:
            raise ValueError("Cylindrée invalide pour une moto")
        self.cylindree = cylindree
    
    @property
    def categorie(self) -> CategorieVehicule:
        return CategorieVehicule.MOTO
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['cylindree'] = self.cylindree
        return data


class Utilitaire(Vehicule):
    """Classe représentant un véhicule utilitaire."""
    
    def __init__(
        self,
        immatriculation: str,
        marque: str,
        modele: str,
        annee: int,
        capacite_charge: float = 1000.0,
        **kwargs
    ):
        super().__init__(immatriculation, marque, modele, annee, **kwargs)
        if capacite_charge < 0:
            raise ValueError("Capacité de charge invalide")
        self.capacite_charge = capacite_charge
    
    @property
    def categorie(self) -> CategorieVehicule:
        return CategorieVehicule.UTILITAIRE
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['capacite_charge'] = self.capacite_charge
        return data


def creer_vehicule_depuis_dict(data: Dict[str, Any]) -> Vehicule:
    """
    Crée un véhicule à partir d'un dictionnaire.
    
    Args:
        data: Dictionnaire contenant les données du véhicule
        
    Returns:
        Instance de la classe appropriée (Voiture, Moto ou Utilitaire)
        
    Raises:
        ValueError: Si la catégorie est invalide
    """
    # Faire une copie pour ne pas modifier l'original
    data = data.copy()
    
    categorie = data.pop('categorie')
    date_ajout = data.pop('date_ajout', None)
    
    # Convertir l'état en EtatVehicule
    if 'etat' in data and isinstance(data['etat'], str):
        data['etat'] = EtatVehicule(data['etat'])
    
    # S'assurer que cout_maintenance et cout_carburant existent
    if 'cout_maintenance' not in data:
        data['cout_maintenance'] = 0.0
    if 'cout_carburant' not in data:
        data['cout_carburant'] = 0.0
    
    # Créer le véhicule selon sa catégorie
    if categorie == CategorieVehicule.VOITURE.value:
        vehicule = Voiture(**data)
    elif categorie == CategorieVehicule.MOTO.value:
        vehicule = Moto(**data)
    elif categorie == CategorieVehicule.UTILITAIRE.value:
        vehicule = Utilitaire(**data)
    else:
        raise ValueError(f"Catégorie inconnue: {categorie}")
    
    # Restaurer la date d'ajout si elle existe
    if date_ajout:
        vehicule.date_ajout = datetime.fromisoformat(date_ajout)
    
    return vehicule