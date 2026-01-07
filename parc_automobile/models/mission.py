"""
Module de définition de la classe Mission.
Gère les missions effectuées par les véhicules.
"""

from datetime import datetime, date
from typing import Optional, Dict, Any
from enum import Enum
import uuid


class StatutMission(Enum):
    """Énumération des statuts possibles d'une mission."""
    PLANIFIEE = "planifiee"
    EN_COURS = "en_cours"
    TERMINEE = "terminee"
    ANNULEE = "annulee"


class Mission:
    """Classe représentant une mission effectuée par un véhicule."""
    
    def __init__(
        self,
        immatriculation_vehicule: str,
        conducteur: str,
        date_mission: date,
        distance: float,
        destination: str,
        cout_carburant: float = 0.0,
        description: str = "",
        statut: StatutMission = StatutMission.PLANIFIEE,
        mission_id: Optional[str] = None
    ):
        """
        Initialise une mission.
        
        Args:
            immatriculation_vehicule: Immatriculation du véhicule utilisé
            conducteur: Nom du conducteur
            date_mission: Date de la mission
            distance: Distance parcourue en km
            destination: Destination de la mission
            cout_carburant: Coût du carburant pour cette mission
            description: Description optionnelle de la mission
            statut: Statut de la mission
            mission_id: Identifiant unique (généré automatiquement si non fourni)
            
        Raises:
            ValueError: Si les paramètres sont invalides
        """
        self._valider_parametres(
            immatriculation_vehicule, conducteur, distance, cout_carburant
        )
        
        self.mission_id = mission_id if mission_id else str(uuid.uuid4())
        self.immatriculation_vehicule = immatriculation_vehicule.upper()
        self.conducteur = conducteur.strip()
        self.date_mission = date_mission if isinstance(date_mission, date) else date.fromisoformat(date_mission)
        self.distance = distance
        self.destination = destination.strip()
        self.cout_carburant = cout_carburant
        self.description = description.strip()
        self.statut = statut if isinstance(statut, StatutMission) else StatutMission(statut)
        self.date_creation = datetime.now()
    
    def _valider_parametres(self, immat: str, conducteur: str, distance: float, cout: float):
        """Valide les paramètres de la mission."""
        if not immat or len(immat.strip()) == 0:
            raise ValueError("L'immatriculation ne peut pas être vide")
        
        if not conducteur or len(conducteur.strip()) == 0:
            raise ValueError("Le nom du conducteur ne peut pas être vide")
        
        if distance < 0:
            raise ValueError("La distance ne peut pas être négative")
        
        if cout < 0:
            raise ValueError("Le coût ne peut pas être négatif")
    
    @property
    def consommation_aux_100(self) -> Optional[float]:
        """
        Calcule la consommation aux 100 km.
        
        Returns:
            Consommation en litres/100km ou None si impossible à calculer
        """
        if self.distance == 0 or self.cout_carburant == 0:
            return None
        
        # Estimation: prix moyen du carburant à 1.80€/L
        PRIX_MOYEN_CARBURANT = 1.80
        litres_consommes = self.cout_carburant / PRIX_MOYEN_CARBURANT
        return (litres_consommes / self.distance) * 100
    
    def changer_statut(self, nouveau_statut: StatutMission):
        """Change le statut de la mission."""
        if not isinstance(nouveau_statut, StatutMission):
            nouveau_statut = StatutMission(nouveau_statut)
        self.statut = nouveau_statut
    
    def terminer_mission(self):
        """Marque la mission comme terminée."""
        self.statut = StatutMission.TERMINEE
    
    def annuler_mission(self):
        """Annule la mission."""
        self.statut = StatutMission.ANNULEE
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit la mission en dictionnaire."""
        return {
            'mission_id': self.mission_id,
            'immatriculation_vehicule': self.immatriculation_vehicule,
            'conducteur': self.conducteur,
            'date_mission': self.date_mission.isoformat(),
            'distance': self.distance,
            'destination': self.destination,
            'cout_carburant': self.cout_carburant,
            'description': self.description,
            'statut': self.statut.value,
            'date_creation': self.date_creation.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Mission':
        """
        Crée une mission à partir d'un dictionnaire.
        
        Args:
            data: Dictionnaire contenant les données de la mission
            
        Returns:
            Instance de Mission
        """
        # Convertir les dates
        if isinstance(data.get('date_mission'), str):
            data['date_mission'] = date.fromisoformat(data['date_mission'])
        
        # Convertir le statut
        if isinstance(data.get('statut'), str):
            data['statut'] = StatutMission(data['statut'])
        
        # Extraire la date de création
        date_creation = data.pop('date_creation', None)
        
        # Créer la mission
        mission = Mission(**data)
        
        # Restaurer la date de création
        if date_creation:
            mission.date_creation = datetime.fromisoformat(date_creation)
        
        return mission
    
    def __str__(self) -> str:
        return (f"Mission {self.mission_id[:8]} - {self.conducteur} - "
                f"{self.date_mission} - {self.distance}km vers {self.destination}")
    
    def __repr__(self) -> str:
        return (f"Mission(mission_id='{self.mission_id}', "
                f"vehicule='{self.immatriculation_vehicule}', "
                f"conducteur='{self.conducteur}')")