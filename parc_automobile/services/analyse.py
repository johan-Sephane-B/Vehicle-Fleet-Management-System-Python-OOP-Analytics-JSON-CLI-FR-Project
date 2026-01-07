"""
Service d'analyse et de statistiques du parc automobile.
Calcule les métriques avancées et génère des rapports.
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime, date
from collections import defaultdict
from models.vehicule import Vehicule, CategorieVehicule
from models.mission import Mission, StatutMission


class AnalyseurParc:
    """Analyseur de données du parc automobile."""
    
    def __init__(self, vehicules: Dict[str, Vehicule], missions: List[Mission]):
        """
        Initialise l'analyseur.
        
        Args:
            vehicules: Dictionnaire des véhicules (clé = immatriculation)
            missions: Liste des missions
        """
        self.vehicules = vehicules
        self.missions = missions
    
    def cout_total_par_vehicule(self) -> Dict[str, float]:
        """
        Calcule le coût total pour chaque véhicule.
        
        Returns:
            Dictionnaire {immatriculation: coût total}
        """
        return {
            immat: vehicule.cout_total 
            for immat, vehicule in self.vehicules.items()
        }
    
    def distance_parcourue_par_vehicule(self) -> Dict[str, float]:
        """
        Calcule la distance totale parcourue par chaque véhicule.
        
        Returns:
            Dictionnaire {immatriculation: distance totale}
        """
        distances = defaultdict(float)
        
        for mission in self.missions:
            if mission.statut == StatutMission.TERMINEE:
                distances[mission.immatriculation_vehicule] += mission.distance
        
        return dict(distances)
    
    def frequence_utilisation_vehicules(self) -> Dict[str, int]:
        """
        Calcule le nombre de missions par véhicule.
        
        Returns:
            Dictionnaire {immatriculation: nombre de missions}
        """
        frequences = defaultdict(int)
        
        for mission in self.missions:
            if mission.statut in [StatutMission.TERMINEE, StatutMission.EN_COURS]:
                frequences[mission.immatriculation_vehicule] += 1
        
        return dict(frequences)
    
    def cout_moyen_par_kilometre(self) -> Dict[str, float]:
        """
        Calcule le coût moyen par kilomètre pour chaque véhicule.
        
        Returns:
            Dictionnaire {immatriculation: coût/km}
        """
        couts_par_km = {}
        distances = self.distance_parcourue_par_vehicule()
        
        for immat, vehicule in self.vehicules.items():
            distance_totale = distances.get(immat, 0) + vehicule.kilometrage
            if distance_totale > 0:
                couts_par_km[immat] = vehicule.cout_total / distance_totale
            else:
                couts_par_km[immat] = 0.0
        
        return couts_par_km
    
    def statistiques_mensuelles(self, annee: int, mois: int) -> Dict[str, Any]:
        """
        Génère des statistiques pour un mois donné.
        
        Args:
            annee: Année
            mois: Mois (1-12)
            
        Returns:
            Dictionnaire contenant les statistiques mensuelles
        """
        missions_mois = [
            m for m in self.missions
            if m.date_mission.year == annee and m.date_mission.month == mois
        ]
        
        if not missions_mois:
            return {
                'nombre_missions': 0,
                'distance_totale': 0,
                'cout_carburant_total': 0,
                'vehicules_utilises': 0,
                'conducteurs_actifs': 0
            }
        
        return {
            'nombre_missions': len(missions_mois),
            'distance_totale': sum(m.distance for m in missions_mois),
            'cout_carburant_total': sum(m.cout_carburant for m in missions_mois),
            'distance_moyenne': sum(m.distance for m in missions_mois) / len(missions_mois),
            'vehicules_utilises': len(set(m.immatriculation_vehicule for m in missions_mois)),
            'conducteurs_actifs': len(set(m.conducteur for m in missions_mois)),
            'missions_par_statut': self._compter_par_statut(missions_mois)
        }
    
    def _compter_par_statut(self, missions: List[Mission]) -> Dict[str, int]:
        """Compte les missions par statut."""
        compteur = defaultdict(int)
        for mission in missions:
            compteur[mission.statut.value] += 1
        return dict(compteur)
    
    def statistiques_annuelles(self, annee: int) -> Dict[int, Dict[str, Any]]:
        """
        Génère des statistiques pour chaque mois d'une année.
        
        Args:
            annee: Année à analyser
            
        Returns:
            Dictionnaire {mois: statistiques}
        """
        stats = {}
        for mois in range(1, 13):
            stats[mois] = self.statistiques_mensuelles(annee, mois)
        return stats
    
    def top_vehicules_par_utilisation(self, n: int = 5) -> List[Tuple[str, int]]:
        """
        Identifie les véhicules les plus utilisés.
        
        Args:
            n: Nombre de véhicules à retourner
            
        Returns:
            Liste de tuples (immatriculation, nombre de missions)
        """
        frequences = self.frequence_utilisation_vehicules()
        return sorted(frequences.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def top_vehicules_par_distance(self, n: int = 5) -> List[Tuple[str, float]]:
        """
        Identifie les véhicules ayant parcouru le plus de distance.
        
        Args:
            n: Nombre de véhicules à retourner
            
        Returns:
            Liste de tuples (immatriculation, distance totale)
        """
        distances = self.distance_parcourue_par_vehicule()
        return sorted(distances.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def top_vehicules_par_cout(self, n: int = 5) -> List[Tuple[str, float]]:
        """
        Identifie les véhicules les plus coûteux.
        
        Args:
            n: Nombre de véhicules à retourner
            
        Returns:
            Liste de tuples (immatriculation, coût total)
        """
        couts = self.cout_total_par_vehicule()
        return sorted(couts.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def statistiques_par_categorie(self) -> Dict[str, Dict[str, Any]]:
        """
        Calcule des statistiques par catégorie de véhicule.
        
        Returns:
            Dictionnaire {catégorie: statistiques}
        """
        stats_par_cat = {}
        
        for categorie in CategorieVehicule:
            vehicules_cat = [v for v in self.vehicules.values() 
                           if v.categorie == categorie]
            
            if not vehicules_cat:
                stats_par_cat[categorie.value] = {
                    'nombre': 0,
                    'cout_moyen': 0,
                    'kilometrage_moyen': 0,
                    'age_moyen': 0
                }
                continue
            
            stats_par_cat[categorie.value] = {
                'nombre': len(vehicules_cat),
                'cout_moyen': sum(v.cout_total for v in vehicules_cat) / len(vehicules_cat),
                'cout_total': sum(v.cout_total for v in vehicules_cat),
                'kilometrage_moyen': sum(v.kilometrage for v in vehicules_cat) / len(vehicules_cat),
                'kilometrage_total': sum(v.kilometrage for v in vehicules_cat),
                'age_moyen': sum(v.age for v in vehicules_cat) / len(vehicules_cat)
            }
        
        return stats_par_cat
    
    def analyse_conducteurs(self) -> Dict[str, Dict[str, Any]]:
        """
        Analyse les statistiques par conducteur.
        
        Returns:
            Dictionnaire {conducteur: statistiques}
        """
        stats_conducteurs = defaultdict(lambda: {
            'nombre_missions': 0,
            'distance_totale': 0,
            'cout_carburant': 0
        })
        
        for mission in self.missions:
            if mission.statut == StatutMission.TERMINEE:
                stats = stats_conducteurs[mission.conducteur]
                stats['nombre_missions'] += 1
                stats['distance_totale'] += mission.distance
                stats['cout_carburant'] += mission.cout_carburant
        
        # Calculer les moyennes
        for conducteur, stats in stats_conducteurs.items():
            if stats['nombre_missions'] > 0:
                stats['distance_moyenne'] = stats['distance_totale'] / stats['nombre_missions']
                stats['cout_moyen'] = stats['cout_carburant'] / stats['nombre_missions']
        
        return dict(stats_conducteurs)
    
    def taux_utilisation_parc(self, periode_jours: int = 30) -> float:
        """
        Calcule le taux d'utilisation du parc sur une période.
        
        Args:
            periode_jours: Nombre de jours à considérer
            
        Returns:
            Taux d'utilisation en pourcentage
        """
        if not self.vehicules:
            return 0.0
        
        date_limite = date.today()
        date_debut = date(
            date_limite.year, 
            date_limite.month, 
            max(1, date_limite.day - periode_jours)
        )
        
        missions_periode = [
            m for m in self.missions
            if date_debut <= m.date_mission <= date_limite
        ]
        
        if not missions_periode:
            return 0.0
        
        vehicules_utilises = len(set(m.immatriculation_vehicule for m in missions_periode))
        return (vehicules_utilises / len(self.vehicules)) * 100
    
    def generer_rapport_complet(self) -> Dict[str, Any]:
        """
        Génère un rapport complet d'analyse.
        
        Returns:
            Dictionnaire contenant toutes les analyses
        """
        return {
            'date_rapport': datetime.now().isoformat(),
            'total_vehicules': len(self.vehicules),
            'total_missions': len(self.missions),
            'cout_total_parc': sum(v.cout_total for v in self.vehicules.values()),
            'distance_totale': sum(self.distance_parcourue_par_vehicule().values()),
            'top_vehicules_utilisation': self.top_vehicules_par_utilisation(),
            'top_vehicules_distance': self.top_vehicules_par_distance(),
            'top_vehicules_cout': self.top_vehicules_par_cout(),
            'statistiques_categories': self.statistiques_par_categorie(),
            'analyse_conducteurs': self.analyse_conducteurs(),
            'taux_utilisation_30j': self.taux_utilisation_parc(30),
            'cout_moyen_kilometrique': sum(self.cout_moyen_par_kilometre().values()) / 
                                      len(self.cout_moyen_par_kilometre()) 
                                      if self.cout_moyen_par_kilometre() else 0
        }