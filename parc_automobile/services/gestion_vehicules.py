"""
Service de gestion des véhicules.
Gère les opérations CRUD et la logique métier.
"""

from typing import List, Optional, Dict, Any
from models.vehicule import (
    Vehicule, Voiture, Moto, Utilitaire, 
    EtatVehicule, CategorieVehicule, creer_vehicule_depuis_dict
)
from utils.stockage import GestionnaireStockage, StockageException


class VehiculeException(Exception):
    """Exception personnalisée pour les erreurs de gestion de véhicules."""
    pass


class GestionnaireVehicules:
    """Gestionnaire des véhicules du parc automobile."""
    
    def __init__(self, stockage: Optional[GestionnaireStockage] = None):
        """
        Initialise le gestionnaire de véhicules.
        
        Args:
            stockage: Gestionnaire de stockage (créé par défaut si non fourni)
        """
        self.stockage = stockage if stockage else GestionnaireStockage()
        self.vehicules: Dict[str, Vehicule] = {}
        self.charger_vehicules()
    
    def charger_vehicules(self):
        """Charge les véhicules depuis le stockage."""
        try:
            donnees = self.stockage.charger_vehicules()
            self.vehicules = {}
            
            for data in donnees:
                try:
                    vehicule = creer_vehicule_depuis_dict(data)
                    self.vehicules[vehicule.immatriculation] = vehicule
                except Exception as e:
                    print(f"Erreur lors du chargement d'un véhicule: {e}")
        
        except StockageException as e:
            raise VehiculeException(f"Impossible de charger les véhicules: {e}")
    
    def sauvegarder_vehicules(self):
        """Sauvegarde les véhicules dans le stockage."""
        try:
            donnees = [v.to_dict() for v in self.vehicules.values()]
            self.stockage.sauvegarder_vehicules(donnees)
        except StockageException as e:
            raise VehiculeException(f"Impossible de sauvegarder les véhicules: {e}")
    
    def ajouter_vehicule(self, vehicule: Vehicule):
        """
        Ajoute un véhicule au parc.
        
        Args:
            vehicule: Le véhicule à ajouter
            
        Raises:
            VehiculeException: Si le véhicule existe déjà
        """
        if vehicule.immatriculation in self.vehicules:
            raise VehiculeException(
                f"Le véhicule {vehicule.immatriculation} existe déjà"
            )
        
        self.vehicules[vehicule.immatriculation] = vehicule
        self.sauvegarder_vehicules()
    
    def supprimer_vehicule(self, immatriculation: str):
        """
        Supprime un véhicule du parc.
        
        Args:
            immatriculation: Immatriculation du véhicule à supprimer
            
        Raises:
            VehiculeException: Si le véhicule n'existe pas
        """
        immatriculation = immatriculation.upper()
        
        if immatriculation not in self.vehicules:
            raise VehiculeException(
                f"Le véhicule {immatriculation} n'existe pas"
            )
        
        del self.vehicules[immatriculation]
        self.sauvegarder_vehicules()
    
    def obtenir_vehicule(self, immatriculation: str) -> Vehicule:
        """
        Récupère un véhicule par son immatriculation.
        
        Args:
            immatriculation: Immatriculation du véhicule
            
        Returns:
            Le véhicule correspondant
            
        Raises:
            VehiculeException: Si le véhicule n'existe pas
        """
        immatriculation = immatriculation.upper()
        
        if immatriculation not in self.vehicules:
            raise VehiculeException(
                f"Le véhicule {immatriculation} n'existe pas"
            )
        
        return self.vehicules[immatriculation]
    
    def modifier_vehicule(self, immatriculation: str, **modifications):
        """
        Modifie les attributs d'un véhicule.
        
        Args:
            immatriculation: Immatriculation du véhicule
            **modifications: Attributs à modifier
            
        Raises:
            VehiculeException: Si le véhicule n'existe pas ou si l'attribut est invalide
        """
        vehicule = self.obtenir_vehicule(immatriculation)
        
        # Attributs modifiables
        attributs_autorise = {
            'kilometrage', 'etat', 'cout_maintenance', 
            'cout_carburant', 'cout_acquisition'
        }
        
        for attr, valeur in modifications.items():
            if attr not in attributs_autorise:
                raise VehiculeException(f"L'attribut '{attr}' ne peut pas être modifié")
            
            # Validation spéciale pour l'état
            if attr == 'etat':
                if isinstance(valeur, str):
                    valeur = EtatVehicule(valeur)
                vehicule.changer_etat(valeur)
            else:
                setattr(vehicule, attr, valeur)
        
        self.sauvegarder_vehicules()
    
    def lister_vehicules(
        self, 
        categorie: Optional[CategorieVehicule] = None,
        etat: Optional[EtatVehicule] = None
    ) -> List[Vehicule]:
        """
        Liste les véhicules avec filtres optionnels.
        
        Args:
            categorie: Filtrer par catégorie (optionnel)
            etat: Filtrer par état (optionnel)
            
        Returns:
            Liste des véhicules correspondant aux critères
        """
        vehicules = list(self.vehicules.values())
        
        if categorie:
            vehicules = [v for v in vehicules if v.categorie == categorie]
        
        if etat:
            vehicules = [v for v in vehicules if v.etat == etat]
        
        return vehicules
    
    def rechercher_vehicules(self, terme: str) -> List[Vehicule]:
        """
        Recherche des véhicules par terme (marque, modèle, immatriculation).
        
        Args:
            terme: Terme de recherche
            
        Returns:
            Liste des véhicules correspondants
        """
        terme = terme.lower()
        resultats = []
        
        for vehicule in self.vehicules.values():
            if (terme in vehicule.immatriculation.lower() or
                terme in vehicule.marque.lower() or
                terme in vehicule.modele.lower()):
                resultats.append(vehicule)
        
        return resultats
    
    def obtenir_statistiques_parc(self) -> Dict[str, Any]:
        """
        Calcule des statistiques sur le parc automobile.
        
        Returns:
            Dictionnaire contenant les statistiques
        """
        vehicules = list(self.vehicules.values())
        
        if not vehicules:
            return {
                'total': 0,
                'par_categorie': {},
                'par_etat': {},
                'age_moyen': 0,
                'kilometrage_total': 0,
                'cout_total': 0
            }
        
        # Statistiques par catégorie
        par_categorie = {}
        for cat in CategorieVehicule:
            count = len([v for v in vehicules if v.categorie == cat])
            par_categorie[cat.value] = count
        
        # Statistiques par état
        par_etat = {}
        for etat in EtatVehicule:
            count = len([v for v in vehicules if v.etat == etat])
            par_etat[etat.value] = count
        
        return {
            'total': len(vehicules),
            'par_categorie': par_categorie,
            'par_etat': par_etat,
            'age_moyen': sum(v.age for v in vehicules) / len(vehicules),
            'kilometrage_total': sum(v.kilometrage for v in vehicules),
            'kilometrage_moyen': sum(v.kilometrage for v in vehicules) / len(vehicules),
            'cout_total': sum(v.cout_total for v in vehicules),
            'cout_moyen': sum(v.cout_total for v in vehicules) / len(vehicules)
        }
    
    def vehicules_necessitant_maintenance(self, seuil_km: float = 15000) -> List[Vehicule]:
        """
        Identifie les véhicules nécessitant une maintenance.
        
        Args:
            seuil_km: Seuil de kilométrage pour la maintenance
            
        Returns:
            Liste des véhicules dépassant le seuil
        """
        return [v for v in self.vehicules.values() if v.kilometrage >= seuil_km]
    
    def vehicules_par_age(self, age_min: int = 0, age_max: int = 100) -> List[Vehicule]:
        """
        Filtre les véhicules par âge.
        
        Args:
            age_min: Âge minimum en années
            age_max: Âge maximum en années
            
        Returns:
            Liste des véhicules dans la tranche d'âge
        """
        return [v for v in self.vehicules.values() 
                if age_min <= v.age <= age_max]
    
    def nombre_vehicules(self) -> int:
        """Retourne le nombre total de véhicules."""
        return len(self.vehicules)