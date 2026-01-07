"""
Service de gestion des missions.
Gère les opérations CRUD sur les missions et leur lien avec les véhicules.
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime
from collections import defaultdict

from models.mission import Mission, StatutMission
from utils.stockage import GestionnaireStockage, StockageException


class MissionException(Exception):
    """Exception personnalisée pour les erreurs de gestion de missions."""
    pass


class GestionnaireMissions:
    """Gestionnaire des missions du parc automobile."""
    
    def __init__(self, stockage: Optional[GestionnaireStockage] = None):
        """
        Initialise le gestionnaire de missions.
        
        Args:
            stockage: Gestionnaire de stockage (créé par défaut si non fourni)
        """
        self.stockage = stockage if stockage else GestionnaireStockage()
        self.missions: List[Mission] = []
        self.charger_missions()
    
    def charger_missions(self):
        """Charge les missions depuis le stockage."""
        try:
            donnees = self.stockage.charger_missions()
            self.missions = []
            
            for data in donnees:
                try:
                    mission = Mission.from_dict(data)
                    self.missions.append(mission)
                except Exception as e:
                    print(f"Erreur lors du chargement d'une mission: {e}")
        
        except StockageException as e:
            raise MissionException(f"Impossible de charger les missions: {e}")
    
    def sauvegarder_missions(self):
        """Sauvegarde les missions dans le stockage."""
        try:
            donnees = [m.to_dict() for m in self.missions]
            self.stockage.sauvegarder_missions(donnees)
        except StockageException as e:
            raise MissionException(f"Impossible de sauvegarder les missions: {e}")
    
    def ajouter_mission(self, mission: Mission):
        """
        Ajoute une mission.
        
        Args:
            mission: La mission à ajouter
            
        Raises:
            MissionException: Si la mission existe déjà
        """
        # Vérifier que la mission n'existe pas déjà
        if any(m.mission_id == mission.mission_id for m in self.missions):
            raise MissionException(f"Mission {mission.mission_id} existe déjà")
        
        self.missions.append(mission)
        self.sauvegarder_missions()
    
    def supprimer_mission(self, mission_id: str):
        """
        Supprime une mission.
        
        Args:
            mission_id: ID de la mission à supprimer
            
        Raises:
            MissionException: Si la mission n'existe pas
        """
        mission = self.obtenir_mission(mission_id)
        self.missions.remove(mission)
        self.sauvegarder_missions()
    
    def obtenir_mission(self, mission_id: str) -> Mission:
        """
        Récupère une mission par son ID.
        
        Args:
            mission_id: ID de la mission
            
        Returns:
            La mission correspondante
            
        Raises:
            MissionException: Si la mission n'existe pas
        """
        for mission in self.missions:
            if mission.mission_id == mission_id:
                return mission
        
        raise MissionException(f"Mission {mission_id} non trouvée")
    
    def modifier_mission(self, mission_id: str, **modifications):
        """
        Modifie les attributs d'une mission.
        
        Args:
            mission_id: ID de la mission
            **modifications: Attributs à modifier
            
        Raises:
            MissionException: Si la mission n'existe pas ou si l'attribut est invalide
        """
        mission = self.obtenir_mission(mission_id)
        
        # Attributs modifiables
        attributs_autorises = {
            'distance', 'cout_carburant', 'destination', 
            'description', 'statut', 'date_mission'
        }
        
        for attr, valeur in modifications.items():
            if attr not in attributs_autorises:
                raise MissionException(f"L'attribut '{attr}' ne peut pas être modifié")
            
            # Validation spéciale pour le statut
            if attr == 'statut':
                if isinstance(valeur, str):
                    valeur = StatutMission(valeur)
                mission.changer_statut(valeur)
            elif attr == 'date_mission':
                if isinstance(valeur, str):
                    valeur = date.fromisoformat(valeur)
                setattr(mission, attr, valeur)
            else:
                setattr(mission, attr, valeur)
        
        self.sauvegarder_missions()
    
    def lister_missions(
        self,
        immatriculation: Optional[str] = None,
        conducteur: Optional[str] = None,
        statut: Optional[StatutMission] = None,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> List[Mission]:
        """
        Liste les missions avec filtres optionnels.
        
        Args:
            immatriculation: Filtrer par véhicule
            conducteur: Filtrer par conducteur
            statut: Filtrer par statut
            date_debut: Date de début de la période
            date_fin: Date de fin de la période
            
        Returns:
            Liste des missions correspondant aux critères
        """
        missions = self.missions.copy()
        
        if immatriculation:
            missions = [m for m in missions 
                       if m.immatriculation_vehicule == immatriculation.upper()]
        
        if conducteur:
            missions = [m for m in missions 
                       if conducteur.lower() in m.conducteur.lower()]
        
        if statut:
            missions = [m for m in missions if m.statut == statut]
        
        if date_debut:
            missions = [m for m in missions if m.date_mission >= date_debut]
        
        if date_fin:
            missions = [m for m in missions if m.date_mission <= date_fin]
        
        return missions
    
    def missions_par_vehicule(self, immatriculation: str) -> List[Mission]:
        """
        Récupère toutes les missions d'un véhicule.
        
        Args:
            immatriculation: Immatriculation du véhicule
            
        Returns:
            Liste des missions du véhicule
        """
        return self.lister_missions(immatriculation=immatriculation)
    
    def missions_par_conducteur(self, conducteur: str) -> List[Mission]:
        """
        Récupère toutes les missions d'un conducteur.
        
        Args:
            conducteur: Nom du conducteur
            
        Returns:
            Liste des missions du conducteur
        """
        return self.lister_missions(conducteur=conducteur)
    
    def terminer_mission(self, mission_id: str):
        """
        Marque une mission comme terminée.
        
        Args:
            mission_id: ID de la mission à terminer
        """
        mission = self.obtenir_mission(mission_id)
        mission.terminer_mission()
        self.sauvegarder_missions()
    
    def annuler_mission(self, mission_id: str):
        """
        Annule une mission.
        
        Args:
            mission_id: ID de la mission à annuler
        """
        mission = self.obtenir_mission(mission_id)
        mission.annuler_mission()
        self.sauvegarder_missions()
    
    def obtenir_statistiques_missions(self) -> Dict[str, Any]:
        """
        Calcule des statistiques sur les missions.
        
        Returns:
            Dictionnaire contenant les statistiques
        """
        if not self.missions:
            return {
                'total': 0,
                'par_statut': {},
                'distance_totale': 0,
                'cout_total': 0
            }
        
        # Statistiques par statut
        par_statut = defaultdict(int)
        for mission in self.missions:
            par_statut[mission.statut.value] += 1
        
        # Missions terminées uniquement
        missions_terminees = [m for m in self.missions 
                             if m.statut == StatutMission.TERMINEE]
        
        distance_totale = sum(m.distance for m in missions_terminees)
        cout_total = sum(m.cout_carburant for m in missions_terminees)
        
        return {
            'total': len(self.missions),
            'par_statut': dict(par_statut),
            'missions_terminees': len(missions_terminees),
            'distance_totale': distance_totale,
            'distance_moyenne': distance_totale / len(missions_terminees) 
                              if missions_terminees else 0,
            'cout_total': cout_total,
            'cout_moyen': cout_total / len(missions_terminees)
                        if missions_terminees else 0,
            'vehicules_uniques': len(set(m.immatriculation_vehicule 
                                       for m in self.missions)),
            'conducteurs_uniques': len(set(m.conducteur for m in self.missions))
        }
    
    def missions_par_periode(
        self, 
        annee: int, 
        mois: Optional[int] = None
    ) -> List[Mission]:
        """
        Récupère les missions d'une période donnée.
        
        Args:
            annee: Année
            mois: Mois optionnel (1-12)
            
        Returns:
            Liste des missions de la période
        """
        missions = [m for m in self.missions if m.date_mission.year == annee]
        
        if mois:
            missions = [m for m in missions if m.date_mission.month == mois]
        
        return missions
    
    def nombre_missions(self) -> int:
        """Retourne le nombre total de missions."""
        return len(self.missions)
    
    def rechercher_missions(self, terme: str) -> List[Mission]:
        """
        Recherche des missions par terme.
        
        Args:
            terme: Terme de recherche (destination, conducteur)
            
        Returns:
            Liste des missions correspondantes
        """
        terme = terme.lower()
        resultats = []
        
        for mission in self.missions:
            if (terme in mission.destination.lower() or
                terme in mission.conducteur.lower() or
                terme in mission.immatriculation_vehicule.lower()):
                resultats.append(mission)
        
        return resultats