"""
Programme principal de gestion du parc automobile.
Interface en ligne de commande pour interagir avec le système.
"""

import sys
from datetime import date, datetime
from typing import Optional

from models.vehicule import Voiture, Moto, Utilitaire, EtatVehicule, CategorieVehicule
from models.mission import Mission, StatutMission
from services.gestion_vehicules import GestionnaireVehicules, VehiculeException
from services.gestion_missions import GestionnaireMissions, MissionException
from services.analyse import AnalyseurParc
from visualisations.graphiques import GenerateurGraphiques


class InterfaceCLI:
    """Interface en ligne de commande pour le système."""
    
    def __init__(self):
        """Initialise l'interface."""
        self.gestionnaire_vehicules = GestionnaireVehicules()
        self.gestionnaire_missions = GestionnaireMissions()
        self.generateur_graphiques = GenerateurGraphiques()
    
    def afficher_menu_principal(self):
        """Affiche le menu principal."""
        print("\n" + "="*60)
        print("🚗 SYSTÈME DE GESTION DE PARC AUTOMOBILE")
        print("="*60)
        print("1. Gestion des véhicules")
        print("2. Gestion des missions")
        print("3. Analyses et statistiques")
        print("4. Visualisations")
        print("5. Générer un rapport complet")
        print("0. Quitter")
        print("="*60)
    
    def afficher_menu_vehicules(self):
        """Affiche le menu de gestion des véhicules."""
        print("\n--- GESTION DES VÉHICULES ---")
        print("1. Ajouter un véhicule")
        print("2. Lister les véhicules")
        print("3. Rechercher un véhicule")
        print("4. Modifier un véhicule")
        print("5. Supprimer un véhicule")
        print("6. Statistiques du parc")
        print("0. Retour")
    
    def afficher_menu_missions(self):
        """Affiche le menu de gestion des missions."""
        print("\n--- GESTION DES MISSIONS ---")
        print("1. Créer une mission")
        print("2. Lister les missions")
        print("3. Missions par véhicule")
        print("4. Missions par conducteur")
        print("5. Terminer une mission")
        print("6. Annuler une mission")
        print("0. Retour")
    
    def afficher_menu_analyses(self):
        """Affiche le menu d'analyses."""
        print("\n--- ANALYSES ET STATISTIQUES ---")
        print("1. Coûts par véhicule")
        print("2. Distances parcourues")
        print("3. Fréquence d'utilisation")
        print("4. Statistiques mensuelles")
        print("5. Top véhicules")
        print("6. Analyse des conducteurs")
        print("7. Statistiques par catégorie")
        print("0. Retour")
    
    def afficher_menu_visualisations(self):
        """Affiche le menu des visualisations."""
        print("\n--- VISUALISATIONS ---")
        print("1. Répartition par catégorie")
        print("2. Évolution des coûts")
        print("3. Distance vs Coût")
        print("4. Utilisation mensuelle")
        print("5. Top véhicules (graphique)")
        print("0. Retour")
    
    def ajouter_vehicule(self):
        """Interface pour ajouter un véhicule."""
        print("\n--- AJOUTER UN VÉHICULE ---")
        print("Catégorie: 1=Voiture, 2=Moto, 3=Utilitaire")
        
        try:
            categorie = input("Catégorie: ").strip()
            immat = input("Immatriculation: ").strip()
            marque = input("Marque: ").strip()
            modele = input("Modèle: ").strip()
            annee = int(input("Année: ").strip())
            km = float(input("Kilométrage (défaut=0): ").strip() or "0")
            cout = float(input("Coût d'acquisition (défaut=0): ").strip() or "0")
            
            if categorie == "1":
                places = int(input("Nombre de places (défaut=5): ").strip() or "5")
                vehicule = Voiture(immat, marque, modele, annee, places, 
                                 kilometrage=km, cout_acquisition=cout)
            elif categorie == "2":
                cylindree = int(input("Cylindrée (défaut=125): ").strip() or "125")
                vehicule = Moto(immat, marque, modele, annee, cylindree,
                              kilometrage=km, cout_acquisition=cout)
            elif categorie == "3":
                capacite = float(input("Capacité de charge en kg (défaut=1000): ").strip() or "1000")
                vehicule = Utilitaire(immat, marque, modele, annee, capacite,
                                    kilometrage=km, cout_acquisition=cout)
            else:
                print("❌ Catégorie invalide")
                return
            
            self.gestionnaire_vehicules.ajouter_vehicule(vehicule)
            print(f"✅ Véhicule {immat} ajouté avec succès!")
        
        except ValueError as e:
            print(f"❌ Erreur de saisie: {e}")
        except VehiculeException as e:
            print(f"❌ Erreur: {e}")
    
    def lister_vehicules(self):
        """Affiche la liste des véhicules."""
        print("\n--- LISTE DES VÉHICULES ---")
        
        vehicules = self.gestionnaire_vehicules.lister_vehicules()
        
        if not vehicules:
            print("Aucun véhicule enregistré.")
            return
        
        for v in vehicules:
            print(f"\n{v.immatriculation} - {v.marque} {v.modele} ({v.annee})")
            print(f"  Catégorie: {v.categorie.value.title()}")
            print(f"  État: {v.etat.value.title()}")
            print(f"  Kilométrage: {v.kilometrage:.0f} km")
            print(f"  Coût total: {v.cout_total:.2f} €")
    
    def creer_mission(self):
        """Interface pour créer une mission."""
        print("\n--- CRÉER UNE MISSION ---")
        
        try:
            immat = input("Immatriculation du véhicule: ").strip()
            conducteur = input("Nom du conducteur: ").strip()
            destination = input("Destination: ").strip()
            distance = float(input("Distance (km): ").strip())
            cout_carburant = float(input("Coût carburant (€, défaut=0): ").strip() or "0")
            date_str = input("Date (YYYY-MM-DD, défaut=aujourd'hui): ").strip()
            
            if date_str:
                date_mission = date.fromisoformat(date_str)
            else:
                date_mission = date.today()
            
            mission = Mission(
                immat, conducteur, date_mission, distance,
                destination, cout_carburant
            )
            
            self.gestionnaire_missions.ajouter_mission(mission)
            print(f"✅ Mission créée avec succès! ID: {mission.mission_id[:8]}")
        
        except ValueError as e:
            print(f"❌ Erreur de saisie: {e}")
        except MissionException as e:
            print(f"❌ Erreur: {e}")
    
    def afficher_statistiques_parc(self):
        """Affiche les statistiques du parc."""
        print("\n--- STATISTIQUES DU PARC ---")
        
        stats = self.gestionnaire_vehicules.obtenir_statistiques_parc()
        
        print(f"\n📊 Vue d'ensemble:")
        print(f"  Total véhicules: {stats['total']}")
        print(f"  Âge moyen: {stats['age_moyen']:.1f} ans")
        print(f"  Kilométrage total: {stats['kilometrage_total']:.0f} km")
        print(f"  Kilométrage moyen: {stats['kilometrage_moyen']:.0f} km")
        print(f"  Coût total du parc: {stats['cout_total']:.2f} €")
        print(f"  Coût moyen par véhicule: {stats['cout_moyen']:.2f} €")
        
        print(f"\n🚗 Par catégorie:")
        for cat, count in stats['par_categorie'].items():
            print(f"  {cat.title()}: {count}")
        
        print(f"\n📋 Par état:")
        for etat, count in stats['par_etat'].items():
            print(f"  {etat.replace('_', ' ').title()}: {count}")
    
    def afficher_analyses(self):
        """Affiche les analyses avancées."""
        analyseur = AnalyseurParc(
            self.gestionnaire_vehicules.vehicules,
            self.gestionnaire_missions.missions
        )
        
        while True:
            self.afficher_menu_analyses()
            choix = input("\nChoix: ").strip()
            
            if choix == "0":
                break
            elif choix == "1":
                self._afficher_couts_vehicules(analyseur)
            elif choix == "2":
                self._afficher_distances(analyseur)
            elif choix == "3":
                self._afficher_frequences(analyseur)
            elif choix == "4":
                self._afficher_stats_mensuelles(analyseur)
            elif choix == "5":
                self._afficher_top_vehicules(analyseur)
            elif choix == "6":
                self._afficher_analyse_conducteurs(analyseur)
            elif choix == "7":
                self._afficher_stats_categories(analyseur)
            else:
                print("❌ Choix invalide")
    
    def _afficher_couts_vehicules(self, analyseur):
        """Affiche les coûts par véhicule."""
        print("\n--- COÛTS PAR VÉHICULE ---")
        couts = analyseur.cout_total_par_vehicule()
        
        for immat, cout in sorted(couts.items(), key=lambda x: x[1], reverse=True):
            vehicule = self.gestionnaire_vehicules.obtenir_vehicule(immat)
            print(f"{immat} ({vehicule.marque} {vehicule.modele}): {cout:.2f} €")
    
    def _afficher_distances(self, analyseur):
        """Affiche les distances parcourues."""
        print("\n--- DISTANCES PARCOURUES ---")
        distances = analyseur.distance_parcourue_par_vehicule()
        
        for immat, distance in sorted(distances.items(), key=lambda x: x[1], reverse=True):
            vehicule = self.gestionnaire_vehicules.obtenir_vehicule(immat)
            print(f"{immat} ({vehicule.marque} {vehicule.modele}): {distance:.0f} km")
    
    def _afficher_frequences(self, analyseur):
        """Affiche les fréquences d'utilisation."""
        print("\n--- FRÉQUENCE D'UTILISATION ---")
        frequences = analyseur.frequence_utilisation_vehicules()
        
        for immat, freq in sorted(frequences.items(), key=lambda x: x[1], reverse=True):
            vehicule = self.gestionnaire_vehicules.obtenir_vehicule(immat)
            print(f"{immat} ({vehicule.marque} {vehicule.modele}): {freq} missions")
    
    def _afficher_stats_mensuelles(self, analyseur):
        """Affiche les statistiques mensuelles."""
        try:
            annee = int(input("Année: ").strip())
            mois = int(input("Mois (1-12): ").strip())
            
            print(f"\n--- STATISTIQUES {mois}/{annee} ---")
            stats = analyseur.statistiques_mensuelles(annee, mois)
            
            print(f"Nombre de missions: {stats['nombre_missions']}")
            print(f"Distance totale: {stats['distance_totale']:.0f} km")
            print(f"Coût carburant: {stats['cout_carburant_total']:.2f} €")
            
            if stats['nombre_missions'] > 0:
                print(f"Distance moyenne: {stats['distance_moyenne']:.0f} km")
                print(f"Véhicules utilisés: {stats['vehicules_utilises']}")
                print(f"Conducteurs actifs: {stats['conducteurs_actifs']}")
        
        except ValueError:
            print("❌ Saisie invalide")
    
    def _afficher_top_vehicules(self, analyseur):
        """Affiche les top véhicules."""
        print("\n--- TOP 5 VÉHICULES ---")
        
        print("\n🔹 Par utilisation:")
        for immat, count in analyseur.top_vehicules_par_utilisation(5):
            print(f"  {immat}: {count} missions")
        
        print("\n🔹 Par distance:")
        for immat, distance in analyseur.top_vehicules_par_distance(5):
            print(f"  {immat}: {distance:.0f} km")
        
        print("\n🔹 Par coût:")
        for immat, cout in analyseur.top_vehicules_par_cout(5):
            print(f"  {immat}: {cout:.2f} €")
    
    def _afficher_analyse_conducteurs(self, analyseur):
        """Affiche l'analyse des conducteurs."""
        print("\n--- ANALYSE DES CONDUCTEURS ---")
        stats = analyseur.analyse_conducteurs()
        
        for conducteur, data in sorted(stats.items(), 
                                      key=lambda x: x[1]['nombre_missions'], 
                                      reverse=True):
            print(f"\n{conducteur}:")
            print(f"  Missions: {data['nombre_missions']}")
            print(f"  Distance totale: {data['distance_totale']:.0f} km")
            print(f"  Distance moyenne: {data.get('distance_moyenne', 0):.0f} km")
            print(f"  Coût carburant: {data['cout_carburant']:.2f} €")
    
    def _afficher_stats_categories(self, analyseur):
        """Affiche les statistiques par catégorie."""
        print("\n--- STATISTIQUES PAR CATÉGORIE ---")
        stats = analyseur.statistiques_par_categorie()
        
        for categorie, data in stats.items():
            print(f"\n{categorie.upper()}:")
            print(f"  Nombre: {data['nombre']}")
            if data['nombre'] > 0:
                print(f"  Coût moyen: {data['cout_moyen']:.2f} €")
                print(f"  Coût total: {data['cout_total']:.2f} €")
                print(f"  Kilométrage moyen: {data['kilometrage_moyen']:.0f} km")
                print(f"  Âge moyen: {data['age_moyen']:.1f} ans")
    
    def generer_visualisations(self):
        """Génère les visualisations."""
        analyseur = AnalyseurParc(
            self.gestionnaire_vehicules.vehicules,
            self.gestionnaire_missions.missions
        )
        
        while True:
            self.afficher_menu_visualisations()
            choix = input("\nChoix: ").strip()
            
            if choix == "0":
                break
            elif choix == "1":
                self.generateur_graphiques.graphique_repartition_categories(
                    self.gestionnaire_vehicules.vehicules
                )
            elif choix == "2":
                self.generateur_graphiques.graphique_evolution_couts(
                    self.gestionnaire_missions.missions
                )
            elif choix == "3":
                self.generateur_graphiques.graphique_distance_vs_cout(
                    self.gestionnaire_vehicules.vehicules,
                    analyseur
                )
            elif choix == "4":
                annee = int(input("Année: ").strip())
                self.generateur_graphiques.graphique_utilisation_mensuelle(
                    self.gestionnaire_missions.missions, annee
                )
            elif choix == "5":
                self.generateur_graphiques.graphique_top_vehicules(analyseur)
            else:
                print("❌ Choix invalide")
    
    def generer_rapport_complet(self):
        """Génère un rapport complet."""
        print("\n--- GÉNÉRATION DU RAPPORT ---")
        
        analyseur = AnalyseurParc(
            self.gestionnaire_vehicules.vehicules,
            self.gestionnaire_missions.missions
        )
        
        rapport = analyseur.generer_rapport_complet()
        
        # Sauvegarder en JSON
        import json
        nom_fichier = f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Rapport sauvegardé: {nom_fichier}")
        
        # Afficher un résumé
        print(f"\n📊 RÉSUMÉ:")
        print(f"  Véhicules: {rapport['total_vehicules']}")
        print(f"  Missions: {rapport['total_missions']}")
        print(f"  Coût total: {rapport['cout_total_parc']:.2f} €")
        print(f"  Distance totale: {rapport['distance_totale']:.0f} km")
        print(f"  Taux d'utilisation (30j): {rapport['taux_utilisation_30j']:.1f}%")
    
    def executer(self):
        """Exécute la boucle principale."""
        print("Bienvenue dans le système de gestion de parc automobile!")
        
        while True:
            self.afficher_menu_principal()
            choix = input("\nVotre choix: ").strip()
            
            if choix == "0":
                print("👋 Au revoir!")
                break
            elif choix == "1":
                self.menu_vehicules()
            elif choix == "2":
                self.menu_missions()
            elif choix == "3":
                self.afficher_analyses()
            elif choix == "4":
                self.generer_visualisations()
            elif choix == "5":
                self.generer_rapport_complet()
            else:
                print("❌ Choix invalide")
    
    def menu_vehicules(self):
        """Menu de gestion des véhicules."""
        while True:
            self.afficher_menu_vehicules()
            choix = input("\nChoix: ").strip()
            
            if choix == "0":
                break
            elif choix == "1":
                self.ajouter_vehicule()
            elif choix == "2":
                self.lister_vehicules()
            elif choix == "6":
                self.afficher_statistiques_parc()
            else:
                print("❌ Fonctionnalité à implémenter")
    
    def menu_missions(self):
        """Menu de gestion des missions."""
        while True:
            self.afficher_menu_missions()
            choix = input("\nChoix: ").strip()
            
            if choix == "0":
                break
            elif choix == "1":
                self.creer_mission()
            else:
                print("❌ Fonctionnalité à implémenter")


def main():
    """Point d'entrée principal."""
    try:
        interface = InterfaceCLI()
        interface.executer()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programme interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()