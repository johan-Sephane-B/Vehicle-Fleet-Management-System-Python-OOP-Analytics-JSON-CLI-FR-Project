"""
Module de gestion du stockage des données en JSON.
Gère la persistance des véhicules et missions.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class StockageException(Exception):
    """Exception personnalisée pour les erreurs de stockage."""
    pass


class GestionnaireStockage:
    """Gestionnaire de stockage des données en JSON."""
    
    def __init__(self, repertoire_data: str = "data"):
        """
        Initialise le gestionnaire de stockage.
        
        Args:
            repertoire_data: Chemin du répertoire de stockage
        """
        self.repertoire_data = Path(repertoire_data)
        self.fichier_vehicules = self.repertoire_data / "vehicules.json"
        self.fichier_missions = self.repertoire_data / "missions.json"
        self.fichier_backup = self.repertoire_data / "backup"
        
        # Créer le répertoire si nécessaire
        self._initialiser_repertoire()
    
    def _initialiser_repertoire(self):
        """Crée le répertoire de données s'il n'existe pas."""
        try:
            self.repertoire_data.mkdir(parents=True, exist_ok=True)
            self.fichier_backup.mkdir(exist_ok=True)
        except Exception as e:
            raise StockageException(f"Impossible de créer le répertoire: {e}")
    
    def sauvegarder_vehicules(self, vehicules: List[Dict[str, Any]]):
        """
        Sauvegarde la liste des véhicules.
        
        Args:
            vehicules: Liste de dictionnaires représentant les véhicules
            
        Raises:
            StockageException: En cas d'erreur de sauvegarde
        """
        try:
            # Créer un backup avant la sauvegarde
            if self.fichier_vehicules.exists():
                self._creer_backup(self.fichier_vehicules, "vehicules")
            
            # Sauvegarder les données
            with open(self.fichier_vehicules, 'w', encoding='utf-8') as f:
                json.dump(vehicules, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            raise StockageException(f"Erreur lors de la sauvegarde des véhicules: {e}")
    
    def charger_vehicules(self) -> List[Dict[str, Any]]:
        """
        Charge la liste des véhicules.
        
        Returns:
            Liste de dictionnaires représentant les véhicules
            
        Raises:
            StockageException: En cas d'erreur de chargement
        """
        try:
            if not self.fichier_vehicules.exists():
                return []
            
            with open(self.fichier_vehicules, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        except json.JSONDecodeError as e:
            raise StockageException(f"Fichier JSON invalide: {e}")
        except Exception as e:
            raise StockageException(f"Erreur lors du chargement des véhicules: {e}")
    
    def sauvegarder_missions(self, missions: List[Dict[str, Any]]):
        """
        Sauvegarde la liste des missions.
        
        Args:
            missions: Liste de dictionnaires représentant les missions
            
        Raises:
            StockageException: En cas d'erreur de sauvegarde
        """
        try:
            # Créer un backup avant la sauvegarde
            if self.fichier_missions.exists():
                self._creer_backup(self.fichier_missions, "missions")
            
            # Sauvegarder les données
            with open(self.fichier_missions, 'w', encoding='utf-8') as f:
                json.dump(missions, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            raise StockageException(f"Erreur lors de la sauvegarde des missions: {e}")
    
    def charger_missions(self) -> List[Dict[str, Any]]:
        """
        Charge la liste des missions.
        
        Returns:
            Liste de dictionnaires représentant les missions
            
        Raises:
            StockageException: En cas d'erreur de chargement
        """
        try:
            if not self.fichier_missions.exists():
                return []
            
            with open(self.fichier_missions, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        except json.JSONDecodeError as e:
            raise StockageException(f"Fichier JSON invalide: {e}")
        except Exception as e:
            raise StockageException(f"Erreur lors du chargement des missions: {e}")
    
    def _creer_backup(self, fichier: Path, nom_type: str):
        """
        Crée une copie de sauvegarde d'un fichier.
        
        Args:
            fichier: Chemin du fichier à sauvegarder
            nom_type: Type de fichier (vehicules ou missions)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.fichier_backup / f"{nom_type}_{timestamp}.json"
            
            # Copier le fichier
            with open(fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(contenu)
            
            # Garder seulement les 5 derniers backups
            self._nettoyer_backups(nom_type)
        
        except Exception:
            # Les erreurs de backup ne doivent pas bloquer l'application
            pass
    
    def _nettoyer_backups(self, nom_type: str, max_backups: int = 5):
        """
        Supprime les anciens backups pour garder seulement les plus récents.
        
        Args:
            nom_type: Type de fichier (vehicules ou missions)
            max_backups: Nombre maximum de backups à conserver
        """
        try:
            # Lister tous les backups du type spécifié
            backups = sorted(
                self.fichier_backup.glob(f"{nom_type}_*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            # Supprimer les backups en excès
            for backup in backups[max_backups:]:
                backup.unlink()
        
        except Exception:
            # Les erreurs de nettoyage ne doivent pas bloquer l'application
            pass
    
    def exporter_csv(self, fichier_sortie: str, donnees: List[Dict[str, Any]], 
                     colonnes: List[str]):
        """
        Exporte des données au format CSV.
        
        Args:
            fichier_sortie: Chemin du fichier CSV de sortie
            donnees: Liste de dictionnaires à exporter
            colonnes: Liste des colonnes à exporter
            
        Raises:
            StockageException: En cas d'erreur d'export
        """
        try:
            import csv
            
            with open(fichier_sortie, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=colonnes, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(donnees)
        
        except Exception as e:
            raise StockageException(f"Erreur lors de l'export CSV: {e}")
    
    def reinitialiser(self):
        """Supprime tous les fichiers de données (utiliser avec précaution!)."""
        try:
            if self.fichier_vehicules.exists():
                self._creer_backup(self.fichier_vehicules, "vehicules")
                self.fichier_vehicules.unlink()
            
            if self.fichier_missions.exists():
                self._creer_backup(self.fichier_missions, "missions")
                self.fichier_missions.unlink()
        
        except Exception as e:
            raise StockageException(f"Erreur lors de la réinitialisation: {e}")
    
    def obtenir_statistiques_stockage(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur le stockage.
        
        Returns:
            Dictionnaire contenant les statistiques
        """
        stats = {
            'vehicules_existe': self.fichier_vehicules.exists(),
            'missions_existe': self.fichier_missions.exists(),
            'nombre_backups': len(list(self.fichier_backup.glob("*.json")))
        }
        
        if stats['vehicules_existe']:
            stats['taille_vehicules'] = self.fichier_vehicules.stat().st_size
        
        if stats['missions_existe']:
            stats['taille_missions'] = self.fichier_missions.stat().st_size
        
        return stats