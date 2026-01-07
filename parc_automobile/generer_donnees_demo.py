"""
Script pour générer des données de démonstration MASSIVES.
Crée un parc automobile complet avec historique riche.
"""
import json
import os
from datetime import date, timedelta
from random import randint, choice, uniform, shuffle

# Créer le répertoire data s'il n'existe pas
os.makedirs("data", exist_ok=True)

print("🚀 Génération MASSIVE de données de démonstration...\n")

# ============================================
# DONNÉES DE BASE
# ============================================

# Marques et modèles par catégorie
voitures_modeles = {
    "Renault": ["Clio", "Megane", "Captur", "Arkana", "Austral"],
    "Peugeot": ["208", "308", "2008", "3008", "5008"],
    "Citroën": ["C3", "C4", "C5 Aircross", "Berlingo"],
    "Volkswagen": ["Polo", "Golf", "Tiguan", "T-Roc"],
    "Toyota": ["Yaris", "Corolla", "RAV4", "Aygo X"],
    "BMW": ["Série 1", "Série 3", "X1", "X3"],
    "Mercedes": ["Classe A", "Classe C", "GLA", "GLB"],
    "Audi": ["A1", "A3", "Q2", "Q3"],
    "Ford": ["Fiesta", "Focus", "Puma", "Kuga"],
    "Opel": ["Corsa", "Astra", "Crossland", "Grandland"],
}

motos_modeles = {
    "Yamaha": ["MT-07", "MT-09", "XSR700", "Tracer 7"],
    "Honda": ["CB500F", "CB650R", "NC750X", "CBR650R"],
    "Kawasaki": ["Z650", "Z900", "Ninja 650", "Versys 650"],
    "Suzuki": ["SV650", "GSX-S750", "V-Strom 650"],
    "BMW": ["F750GS", "F850GS", "S1000RR"],
    "Ducati": ["Monster 821", "Scrambler 800", "Multistrada 950"],
}

utilitaires_modeles = {
    "Renault": ["Master", "Trafic", "Kangoo"],
    "Peugeot": ["Expert", "Boxer", "Partner"],
    "Citroën": ["Jumper", "Jumpy", "Berlingo Van"],
    "Fiat": ["Ducato", "Fiorino", "Doblo Cargo"],
    "Mercedes": ["Sprinter", "Vito", "Citan"],
    "Volkswagen": ["Crafter", "Transporter", "Caddy"],
    "Ford": ["Transit", "Transit Custom", "Transit Connect"],
}

# Destinations françaises variées
destinations = [
    "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Strasbourg",
    "Montpellier", "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre", "Toulon",
    "Grenoble", "Dijon", "Angers", "Saint-Étienne", "Brest", "Le Mans", "Amiens",
    "Tours", "Limoges", "Clermont-Ferrand", "Villeurbanne", "Besançon", "Orléans",
    "Rouen", "Mulhouse", "Caen", "Nancy", "Saint-Denis", "Argenteuil", "Montreuil",
    "Roubaix", "Dunkerque", "Avignon", "Nîmes", "Poitiers", "Aix-en-Provence"
]

# Prénoms et noms français
prenoms = [
    "Jean", "Marie", "Pierre", "Sophie", "Luc", "Claire", "Michel", "Isabelle",
    "Philippe", "Christine", "François", "Nathalie", "Laurent", "Sandrine",
    "Alain", "Catherine", "Thierry", "Véronique", "Patrick", "Sylvie",
    "Bernard", "Martine", "Jacques", "Monique", "André", "Nicole", "Daniel",
    "Françoise", "Christian", "Brigitte", "Marc", "Annie", "Paul", "Dominique",
    "Nicolas", "Christelle", "Julien", "Stéphanie", "Thomas", "Céline",
    "Alexandre", "Julie", "David", "Aurélie", "Sébastien", "Mélanie",
    "Maxime", "Laura", "Antoine", "Marine", "Lucas", "Camille"
]

noms = [
    "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Petit", "Richard",
    "Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre", "Michel",
    "Garcia", "David", "Bertrand", "Roux", "Vincent", "Fournier", "Morel",
    "Girard", "André", "Mercier", "Dupont", "Lambert", "Bonnet", "François",
    "Martinez", "Legrand", "Garnier", "Faure", "Rousseau", "Blanc", "Guerin",
    "Muller", "Henry", "Roussel", "Nicolas", "Perrin", "Morin", "Mathieu",
    "Clement", "Gauthier", "Dumont", "Lopez", "Fontaine", "Chevalier", "Robin"
]

# Générer liste de conducteurs
conducteurs = [f"{choice(prenoms)} {choice(noms)}" for _ in range(50)]
conducteurs = list(set(conducteurs))[:40]  # 40 conducteurs uniques

etats_possibles = ["disponible", "en_mission", "en_maintenance", "hors_service"]
etats_poids = [0.60, 0.25, 0.10, 0.05]  # 60% dispo, 25% mission, 10% maintenance, 5% HS

# ============================================
# GÉNÉRATION DES VÉHICULES (50 véhicules)
# ============================================

vehicules_demo = []
immat_lettres = "ABCDEFGHJKLMNPRSTUVWXYZ"  # Sans I, O, Q
immat_chiffres = "0123456789"

def generer_immatriculation():
    """Génère une immatriculation unique."""
    while True:
        immat = f"{choice(immat_lettres)}{choice(immat_lettres)}-{randint(100,999)}-{choice(immat_lettres)}{choice(immat_lettres)}"
        if not any(v['immatriculation'] == immat for v in vehicules_demo):
            return immat

# Générer 30 voitures
print("📝 Génération de 30 voitures...")
for i in range(30):
    marque = choice(list(voitures_modeles.keys()))
    modele = choice(voitures_modeles[marque])
    annee = randint(2016, 2023)
    age = 2025 - annee
    
    # Kilométrage basé sur l'âge
    km_moyen_par_an = randint(12000, 25000)
    kilometrage = km_moyen_par_an * age + randint(-5000, 5000)
    kilometrage = max(1000, kilometrage)
    
    # Coûts basés sur l'âge et le kilométrage
    cout_acquisition = randint(12000, 45000)
    cout_maintenance = int(kilometrage * uniform(0.02, 0.05))
    cout_carburant = int(kilometrage * uniform(0.08, 0.14))
    
    # États pondérés
    etat = choice(etats_possibles)
    if uniform(0, 1) < 0.05 and age > 6:  # 5% de chances d'être HS si vieux
        etat = "hors_service"
    
    date_ajout = date(2024, randint(1, 12), randint(1, 28))
    
    vehicules_demo.append({
        "immatriculation": generer_immatriculation(),
        "marque": marque,
        "modele": modele,
        "annee": annee,
        "kilometrage": kilometrage,
        "cout_acquisition": cout_acquisition,
        "cout_maintenance": cout_maintenance,
        "cout_carburant": cout_carburant,
        "etat": etat,
        "categorie": "voiture",
        "nombre_places": choice([5, 5, 5, 7]),  # Majorité 5 places
        "date_ajout": date_ajout.isoformat() + "T" + f"{randint(8,18):02d}:{randint(0,59):02d}:00"
    })

# Générer 10 motos
print("📝 Génération de 10 motos...")
for i in range(10):
    marque = choice(list(motos_modeles.keys()))
    modele = choice(motos_modeles[marque])
    annee = randint(2017, 2023)
    age = 2025 - annee
    
    km_moyen_par_an = randint(5000, 12000)
    kilometrage = km_moyen_par_an * age + randint(-2000, 2000)
    kilometrage = max(500, kilometrage)
    
    cout_acquisition = randint(5000, 15000)
    cout_maintenance = int(kilometrage * uniform(0.025, 0.06))
    cout_carburant = int(kilometrage * uniform(0.05, 0.09))
    
    cylindree = choice([500, 650, 700, 750, 800, 900])
    
    etat = choice(["disponible", "disponible", "en_mission"])  # Motos rarement en panne
    
    date_ajout = date(2024, randint(1, 12), randint(1, 28))
    
    vehicules_demo.append({
        "immatriculation": generer_immatriculation(),
        "marque": marque,
        "modele": modele,
        "annee": annee,
        "kilometrage": kilometrage,
        "cout_acquisition": cout_acquisition,
        "cout_maintenance": cout_maintenance,
        "cout_carburant": cout_carburant,
        "etat": etat,
        "categorie": "moto",
        "cylindree": cylindree,
        "date_ajout": date_ajout.isoformat() + "T" + f"{randint(8,18):02d}:{randint(0,59):02d}:00"
    })

# Générer 10 utilitaires
print("📝 Génération de 10 utilitaires...")
for i in range(10):
    marque = choice(list(utilitaires_modeles.keys()))
    modele = choice(utilitaires_modeles[marque])
    annee = randint(2015, 2023)
    age = 2025 - annee
    
    km_moyen_par_an = randint(20000, 45000)  # Utilitaires roulent plus
    kilometrage = km_moyen_par_an * age + randint(-10000, 10000)
    kilometrage = max(5000, kilometrage)
    
    cout_acquisition = randint(20000, 50000)
    cout_maintenance = int(kilometrage * uniform(0.03, 0.07))
    cout_carburant = int(kilometrage * uniform(0.12, 0.18))  # Consomment plus
    
    capacite_charge = choice([1000, 1200, 1500, 1800, 2000, 2500])
    
    # Utilitaires ont plus de chances d'être HS ou en maintenance
    rand = uniform(0, 1)
    if rand < 0.5:
        etat = "disponible"
    elif rand < 0.75:
        etat = "en_mission"
    elif rand < 0.90:
        etat = "en_maintenance"
    else:
        etat = "hors_service"
    
    date_ajout = date(2024, randint(1, 12), randint(1, 28))
    
    vehicules_demo.append({
        "immatriculation": generer_immatriculation(),
        "marque": marque,
        "modele": modele,
        "annee": annee,
        "kilometrage": kilometrage,
        "cout_acquisition": cout_acquisition,
        "cout_maintenance": cout_maintenance,
        "cout_carburant": cout_carburant,
        "etat": etat,
        "categorie": "utilitaire",
        "capacite_charge": capacite_charge,
        "date_ajout": date_ajout.isoformat() + "T" + f"{randint(8,18):02d}:{randint(0,59):02d}:00"
    })

print(f"✅ {len(vehicules_demo)} véhicules générés\n")

# ============================================
# GÉNÉRATION DES MISSIONS (500+ missions)
# ============================================

print("📝 Génération de 500+ missions...")

missions_demo = []
today = date.today()
mission_counter = 0

for v in vehicules_demo:
    # Nombre de missions basé sur le type et l'âge
    if v['categorie'] == 'voiture':
        nb_missions = randint(8, 20)
    elif v['categorie'] == 'moto':
        nb_missions = randint(5, 12)
    else:  # utilitaire
        nb_missions = randint(12, 25)
    
    for i in range(nb_missions):
        # Distribution des statuts
        rand = uniform(0, 1)
        if rand < 0.75:  # 75% terminées
            statut = "terminee"
            jours_ecart = randint(10, 730)  # Sur 2 ans
            d = today - timedelta(days=jours_ecart)
        elif rand < 0.88:  # 13% planifiées
            statut = "planifiee"
            jours_ecart = randint(1, 60)
            d = today + timedelta(days=jours_ecart)
        elif rand < 0.96:  # 8% en cours
            statut = "en_cours"
            jours_ecart = randint(0, 5)
            d = today - timedelta(days=jours_ecart)
        else:  # 4% annulées
            statut = "annulee"
            jours_ecart = randint(5, 365)
            d = today - timedelta(days=jours_ecart)
        
        # Distance basée sur le type de véhicule
        if v['categorie'] == 'moto':
            distance = float(randint(20, 400))
        elif v['categorie'] == 'utilitaire':
            distance = float(randint(50, 800))
        else:  # voiture
            distance = float(randint(30, 1200))
        
        # Coût carburant proportionnel (prix au litre entre 1.60€ et 2.00€)
        if v['categorie'] == 'moto':
            conso_100 = uniform(4.0, 6.0)  # L/100km
        elif v['categorie'] == 'utilitaire':
            conso_100 = uniform(8.0, 12.0)
        else:  # voiture
            conso_100 = uniform(5.0, 9.0)
        
        litres = (distance / 100) * conso_100
        prix_litre = uniform(1.60, 2.00)
        cout = round(litres * prix_litre, 2)
        
        conducteur = choice(conducteurs)
        destination = choice(destinations)
        
        mission_id = f"M{mission_counter:05d}-{v['immatriculation'].replace('-', '')}"
        mission_counter += 1
        
        missions_demo.append({
            "mission_id": mission_id,
            "immatriculation_vehicule": v["immatriculation"],
            "conducteur": conducteur,
            "date_mission": d.isoformat(),
            "distance": distance,
            "destination": destination,
            "cout_carburant": cout,
            "description": f"Mission {statut} vers {destination}",
            "statut": statut,
            "date_creation": (d - timedelta(days=randint(1, 7))).isoformat() + "T" + f"{randint(8,18):02d}:{randint(0,59):02d}:00"
        })

print(f"✅ {len(missions_demo)} missions générées\n")

# ============================================
# SAUVEGARDE
# ============================================

print("💾 Sauvegarde des données...")
with open("data/vehicules.json", "w", encoding="utf-8") as f:
    json.dump(vehicules_demo, f, indent=2, ensure_ascii=False)

with open("data/missions.json", "w", encoding="utf-8") as f:
    json.dump(missions_demo, f, indent=2, ensure_ascii=False)

# ============================================
# STATISTIQUES DÉTAILLÉES
# ============================================

print("\n" + "="*70)
print("✅ GÉNÉRATION MASSIVE TERMINÉE AVEC SUCCÈS !")
print("="*70)

print(f"\n📊 STATISTIQUES DÉTAILLÉES:")
print(f"\n🚗 VÉHICULES ({len(vehicules_demo)} total):")

# Par catégorie
voitures = [v for v in vehicules_demo if v['categorie'] == 'voiture']
motos = [v for v in vehicules_demo if v['categorie'] == 'moto']
utilitaires = [v for v in vehicules_demo if v['categorie'] == 'utilitaire']

print(f"  ├─ Voitures : {len(voitures)}")
print(f"  ├─ Motos : {len(motos)}")
print(f"  └─ Utilitaires : {len(utilitaires)}")

# Par état
print(f"\n📋 Par état:")
etats_count = {}
for v in vehicules_demo:
    etat = v['etat']
    etats_count[etat] = etats_count.get(etat, 0) + 1

for etat, count in sorted(etats_count.items()):
    pct = (count / len(vehicules_demo)) * 100
    print(f"  ├─ {etat.replace('_', ' ').title()} : {count} ({pct:.1f}%)")

# Coûts totaux
cout_total_parc = sum(v['cout_acquisition'] + v['cout_maintenance'] + v['cout_carburant'] for v in vehicules_demo)
km_total_parc = sum(v['kilometrage'] for v in vehicules_demo)

print(f"\n💰 COÛTS:")
print(f"  ├─ Coût total du parc : {cout_total_parc:,.2f} €")
print(f"  ├─ Coût moyen/véhicule : {cout_total_parc/len(vehicules_demo):,.2f} €")
print(f"  └─ Kilométrage total : {km_total_parc:,.0f} km")

# Missions
print(f"\n📍 MISSIONS ({len(missions_demo)} total):")

statuts_count = {}
for m in missions_demo:
    st = m['statut']
    statuts_count[st] = statuts_count.get(st, 0) + 1

for statut, count in sorted(statuts_count.items()):
    pct = (count / len(missions_demo)) * 100
    print(f"  ├─ {statut.replace('_', ' ').title()} : {count} ({pct:.1f}%)")

# Distance et coûts missions
missions_terminees = [m for m in missions_demo if m['statut'] == 'terminee']
if missions_terminees:
    distance_totale = sum(m['distance'] for m in missions_terminees)
    cout_carburant_total = sum(m['cout_carburant'] for m in missions_terminees)
    
    print(f"\n⛽ MISSIONS TERMINÉES:")
    print(f"  ├─ Distance totale : {distance_totale:,.0f} km")
    print(f"  ├─ Distance moyenne : {distance_totale/len(missions_terminees):.0f} km")
    print(f"  ├─ Coût carburant total : {cout_carburant_total:,.2f} €")
    print(f"  └─ Coût moyen/mission : {cout_carburant_total/len(missions_terminees):.2f} €")

print(f"\n👥 AUTRES:")
print(f"  ├─ Conducteurs uniques : {len(conducteurs)}")
print(f"  ├─ Destinations : {len(destinations)}")
print(f"  └─ Période couverte : 2 ans d'historique")

print("\n" + "="*70)
print("💡 Lancez maintenant: python main.py")
print("="*70)