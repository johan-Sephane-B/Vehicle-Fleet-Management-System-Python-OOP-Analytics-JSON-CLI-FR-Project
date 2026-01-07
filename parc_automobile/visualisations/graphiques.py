"""
Module de génération de visualisations avec Matplotlib.
Crée des graphiques professionnels pour l'analyse du parc.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict, List
from datetime import datetime
from collections import defaultdict

from models.vehicule import Vehicule, CategorieVehicule
from models.mission import Mission, StatutMission
from services.analyse import AnalyseurParc


class GenerateurGraphiques:
    """Générateur de graphiques pour l'analyse du parc."""
    
    def __init__(self):
        """Initialise le générateur."""
        # Style par défaut
        plt.style.use('default')
        self.couleurs = {
            'voiture': '#3498db',
            'moto': '#e74c3c',
            'utilitaire': '#2ecc71',
            'disponible': '#27ae60',
            'en_mission': '#f39c12',
            'en_maintenance': '#e67e22',
            'hors_service': '#95a5a6'
        }
    
    def graphique_repartition_categories(self, vehicules: Dict[str, Vehicule]):
        """
        Crée un camembert de la répartition par catégorie.
        
        Args:
            vehicules: Dictionnaire des véhicules
        """
        # Compter par catégorie
        categories = defaultdict(int)
        for vehicule in vehicules.values():
            categories[vehicule.categorie.value] += 1
        
        if not categories:
            print("❌ Aucune donnée à afficher")
            return
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(10, 7))
        
        labels = [cat.title() for cat in categories.keys()]
        sizes = list(categories.values())
        colors = [self.couleurs.get(cat, '#95a5a6') for cat in categories.keys()]
        
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 12}
        )
        
        # Améliorer le style
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Répartition des Véhicules par Catégorie', 
                    fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig('repartition_categories.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique sauvegardé: repartition_categories.png")
        plt.show()
    
    def graphique_evolution_couts(self, missions: List[Mission]):
        """
        Crée un graphique de l'évolution des coûts mensuels.
        
        Args:
            missions: Liste des missions
        """
        missions_terminees = [m for m in missions if m.statut == StatutMission.TERMINEE]
        
        if not missions_terminees:
            print("❌ Aucune mission terminée à afficher")
            return
        
        # Agréger par mois
        couts_mensuels = defaultdict(float)
        for mission in missions_terminees:
            mois_annee = mission.date_mission.strftime('%Y-%m')
            couts_mensuels[mois_annee] += mission.cout_carburant
        
        # Trier par date
        mois_tries = sorted(couts_mensuels.keys())
        couts = [couts_mensuels[mois] for mois in mois_tries]
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(mois_tries, couts, marker='o', linewidth=2, 
               markersize=8, color='#3498db')
        ax.fill_between(range(len(mois_tries)), couts, alpha=0.3, color='#3498db')
        
        ax.set_xlabel('Mois', fontsize=12, fontweight='bold')
        ax.set_ylabel('Coût Carburant (€)', fontsize=12, fontweight='bold')
        ax.set_title('Évolution des Coûts de Carburant Mensuels', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Rotation des labels
        plt.xticks(rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('evolution_couts.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique sauvegardé: evolution_couts.png")
        plt.show()
    
    def graphique_distance_vs_cout(
        self, 
        vehicules: Dict[str, Vehicule],
        analyseur: AnalyseurParc
    ):
        """
        Crée un scatter plot distance vs coût.
        
        Args:
            vehicules: Dictionnaire des véhicules
            analyseur: Analyseur pour les calculs
        """
        distances = analyseur.distance_parcourue_par_vehicule()
        
        if not distances:
            print("❌ Aucune donnée à afficher")
            return
        
        # Préparer les données
        x = []  # distances
        y = []  # coûts
        colors = []
        labels = []
        
        for immat, vehicule in vehicules.items():
            distance = distances.get(immat, 0) + vehicule.kilometrage
            if distance > 0:
                x.append(distance)
                y.append(vehicule.cout_total)
                colors.append(self.couleurs.get(vehicule.categorie.value, '#95a5a6'))
                labels.append(f"{vehicule.marque} {vehicule.modele}")
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(12, 8))
        
        scatter = ax.scatter(x, y, c=colors, s=200, alpha=0.6, edgecolors='black')
        
        # Ajouter les labels
        for i, label in enumerate(labels):
            ax.annotate(label, (x[i], y[i]), fontsize=8, 
                       xytext=(5, 5), textcoords='offset points')
        
        ax.set_xlabel('Distance Totale (km)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Coût Total (€)', fontsize=12, fontweight='bold')
        ax.set_title('Distance Parcourue vs Coût Total par Véhicule', 
                    fontsize=16, fontweight='bold', pad=20)
        
        ax.grid(True, alpha=0.3)
        
        # Légende
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.couleurs['voiture'], label='Voiture'),
            Patch(facecolor=self.couleurs['moto'], label='Moto'),
            Patch(facecolor=self.couleurs['utilitaire'], label='Utilitaire')
        ]
        ax.legend(handles=legend_elements, loc='upper left')
        
        plt.tight_layout()
        plt.savefig('distance_vs_cout.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique sauvegardé: distance_vs_cout.png")
        plt.show()
    
    def graphique_utilisation_mensuelle(self, missions: List[Mission], annee: int):
        """
        Crée un histogramme de l'utilisation mensuelle.
        
        Args:
            missions: Liste des missions
            annee: Année à analyser
        """
        # Filtrer par année
        missions_annee = [m for m in missions if m.date_mission.year == annee]
        
        if not missions_annee:
            print(f"❌ Aucune mission en {annee}")
            return
        
        # Compter par mois
        missions_par_mois = defaultdict(int)
        for i in range(1, 13):
            missions_par_mois[i] = 0
        
        for mission in missions_annee:
            missions_par_mois[mission.date_mission.month] += 1
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(12, 6))
        
        mois = list(range(1, 13))
        noms_mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun',
                     'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        valeurs = [missions_par_mois[m] for m in mois]
        
        bars = ax.bar(noms_mois, valeurs, color='#3498db', alpha=0.7, edgecolor='black')
        
        # Ajouter les valeurs au-dessus des barres
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Mois', fontsize=12, fontweight='bold')
        ax.set_ylabel('Nombre de Missions', fontsize=12, fontweight='bold')
        ax.set_title(f'Utilisation Mensuelle du Parc - {annee}', 
                    fontsize=16, fontweight='bold', pad=20)
        
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(f'utilisation_mensuelle_{annee}.png', dpi=300, bbox_inches='tight')
        print(f"✅ Graphique sauvegardé: utilisation_mensuelle_{annee}.png")
        plt.show()
    
    def graphique_top_vehicules(self, analyseur: AnalyseurParc):
        """
        Crée un graphique en barres des top véhicules.
        
        Args:
            analyseur: Analyseur pour les calculs
        """
        top_utilisation = analyseur.top_vehicules_par_utilisation(10)
        
        if not top_utilisation:
            print("❌ Aucune donnée à afficher")
            return
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(12, 8))
        
        immatriculations = [item[0] for item in top_utilisation]
        valeurs = [item[1] for item in top_utilisation]
        
        bars = ax.barh(immatriculations, valeurs, color='#2ecc71', 
                      alpha=0.7, edgecolor='black')
        
        # Ajouter les valeurs
        for i, (bar, val) in enumerate(zip(bars, valeurs)):
            ax.text(val, i, f' {val}', va='center', fontweight='bold')
        
        ax.set_xlabel('Nombre de Missions', fontsize=12, fontweight='bold')
        ax.set_ylabel('Véhicule', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 des Véhicules les Plus Utilisés', 
                    fontsize=16, fontweight='bold', pad=20)
        
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig('top_vehicules.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique sauvegardé: top_vehicules.png")
        plt.show()
    
    def graphique_etats_parc(self, vehicules: Dict[str, Vehicule]):
        """
        Crée un graphique de la répartition par état.
        
        Args:
            vehicules: Dictionnaire des véhicules
        """
        # Compter par état
        etats = defaultdict(int)
        for vehicule in vehicules.values():
            etats[vehicule.etat.value] += 1
        
        if not etats:
            print("❌ Aucune donnée à afficher")
            return
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(10, 6))
        
        labels = [etat.replace('_', ' ').title() for etat in etats.keys()]
        sizes = list(etats.values())
        colors = [self.couleurs.get(etat, '#95a5a6') for etat in etats.keys()]
        
        bars = ax.bar(labels, sizes, color=colors, alpha=0.7, edgecolor='black')
        
        # Ajouter les valeurs
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Nombre de Véhicules', fontsize=12, fontweight='bold')
        ax.set_title('État Actuel du Parc Automobile', 
                    fontsize=16, fontweight='bold', pad=20)
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=15)
        
        plt.tight_layout()
        plt.savefig('etats_parc.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique sauvegardé: etats_parc.png")
        plt.show()