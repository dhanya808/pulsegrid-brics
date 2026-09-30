"""
PulseGrid BRICS - Realistic Synthetic Grassroots Healthcare Telemetry Dataset
Contains realistic primary healthcare facility data, critical emergency medicines,
bed allocations, medical staff attendance, and outbreak signal telemetry.
"""

from typing import List, Dict, Any
import math

MEDICINE_CATALOG = [
    {"id": "med_antivenom", "name": "Polyvalent Snake Antivenom (10ml)", "category": "Emergency & Trauma", "critical_threshold_days": 4, "unit": "vials", "cold_chain": True},
    {"id": "med_arv", "name": "Anti-Rabies Vaccine (ARV) 2.5 IU", "category": "Vaccines & Biologicals", "critical_threshold_days": 5, "unit": "vials", "cold_chain": True},
    {"id": "med_insulin", "name": "Regular Human Insulin 40 IU/ml", "category": "Endocrine & Chronic", "critical_threshold_days": 6, "unit": "vials", "cold_chain": True},
    {"id": "med_paracetamol_iv", "name": "Paracetamol IV Infusion 100ml", "category": "Analgesics & Antipyretics", "critical_threshold_days": 3, "unit": "bottles", "cold_chain": False},
    {"id": "med_amox_clav", "name": "Amoxicillin + Clavulanate 625mg", "category": "Antibiotics", "critical_threshold_days": 5, "unit": "tablets", "cold_chain": False},
    {"id": "med_ors", "name": "Oral Rehydration Salts (ORS) WHO Formula", "category": "Gastrointestinal", "critical_threshold_days": 4, "unit": "sachets", "cold_chain": False},
    {"id": "med_o2", "name": "Medical Oxygen (40L Cylinder)", "category": "Critical Respiratory", "critical_threshold_days": 2, "unit": "cylinders", "cold_chain": False},
    {"id": "med_delivery_kit", "name": "Disposable Clean Delivery Kit (CDK)", "category": "Maternal & Child", "critical_threshold_days": 5, "unit": "kits", "cold_chain": False},
    {"id": "med_malaria_rdt", "name": "Rapid Diagnostic Test (RDT) Malaria Pf/Pv", "category": "Diagnostics", "critical_threshold_days": 5, "unit": "kits", "cold_chain": False},
    {"id": "med_doxycycline", "name": "Doxycycline 100mg Capsules", "category": "Vector-Borne Prophylaxis", "critical_threshold_days": 5, "unit": "capsules", "cold_chain": False}
]

# 20 Primary Health Centres, Community Health Centres & District Depots across sample Indian Districts
# Representing rural tribal belts (Gadchiroli), agricultural hubs (Wardha), semi-urban (Pune), and riverine flood plains (Varanasi/Gorakhpur)
FACILITIES_SEED: List[Dict[str, Any]] = [
    {
        "id": "PHC-MH-GAD-01",
        "name": "PHC Bhamragad (Tribal Belt)",
        "type": "Primary Health Centre",
        "district": "Gadchiroli",
        "state": "Maharashtra",
        "country": "India",
        "coordinates": {"lat": 19.4674, "lng": 80.3712},
        "coverage_population": 42000,
        "is_remote_access": True,
        "beds": {"total": 12, "occupied": 11, "icu_total": 0, "icu_occupied": 0, "maternity_total": 4, "maternity_occupied": 4},
        "staff": {"doctors_registered": 2, "doctors_on_duty": 1, "nurses_on_duty": 3, "pharmacists_on_duty": 1},
        "footfall": {"today": 184, "yesterday": 162, "seven_day_avg": 95, "surge_detected": True, "surge_reason": "Post-Monsoon Snakebite & Viral Fever Outbreak"},
        "inventory": {
            "med_antivenom": {"stock": 4, "daily_burn": 6, "batch_expiry": "2026-11-30"},
            "med_arv": {"stock": 9, "daily_burn": 4, "batch_expiry": "2027-02-15"},
            "med_insulin": {"stock": 18, "daily_burn": 3, "batch_expiry": "2026-12-10"},
            "med_paracetamol_iv": {"stock": 35, "daily_burn": 30, "batch_expiry": "2027-06-01"},
            "med_amox_clav": {"stock": 420, "daily_burn": 110, "batch_expiry": "2027-04-18"},
            "med_ors": {"stock": 80, "daily_burn": 65, "batch_expiry": "2027-09-01"},
            "med_o2": {"stock": 2, "daily_burn": 2, "batch_expiry": "N/A"},
            "med_delivery_kit": {"stock": 12, "daily_burn": 2, "batch_expiry": "2028-01-01"},
            "med_malaria_rdt": {"stock": 15, "daily_burn": 35, "batch_expiry": "2026-12-31"},
            "med_doxycycline": {"stock": 300, "daily_burn": 80, "batch_expiry": "2027-03-20"}
        }
    },
    {
        "id": "PHC-MH-GAD-02",
        "name": "PHC Aheri",
        "type": "Primary Health Centre",
        "district": "Gadchiroli",
        "state": "Maharashtra",
        "country": "India",
        "coordinates": {"lat": 19.4182, "lng": 80.0031},
        "coverage_population": 38000,
        "is_remote_access": True,
        "beds": {"total": 14, "occupied": 13, "icu_total": 0, "icu_occupied": 0, "maternity_total": 4, "maternity_occupied": 3},
        "staff": {"doctors_registered": 2, "doctors_on_duty": 1, "nurses_on_duty": 2, "pharmacists_on_duty": 1},
        "footfall": {"today": 142, "yesterday": 138, "seven_day_avg": 88, "surge_detected": True, "surge_reason": "Acute Diarrheal Surge & Suspected Cholera"},
        "inventory": {
            "med_antivenom": {"stock": 8, "daily_burn": 3, "batch_expiry": "2026-10-15"},
            "med_arv": {"stock": 14, "daily_burn": 2, "batch_expiry": "2027-01-20"},
            "med_insulin": {"stock": 15, "daily_burn": 2, "batch_expiry": "2026-11-25"},
            "med_paracetamol_iv": {"stock": 40, "daily_burn": 25, "batch_expiry": "2027-05-10"},
            "med_amox_clav": {"stock": 350, "daily_burn": 90, "batch_expiry": "2027-03-15"},
            "med_ors": {"stock": 45, "daily_burn": 85, "batch_expiry": "2027-08-10"},
            "med_o2": {"stock": 3, "daily_burn": 2, "batch_expiry": "N/A"},
            "med_delivery_kit": {"stock": 15, "daily_burn": 3, "batch_expiry": "2028-02-01"},
            "med_malaria_rdt": {"stock": 25, "daily_burn": 20, "batch_expiry": "2026-11-15"},
            "med_doxycycline": {"stock": 210, "daily_burn": 55, "batch_expiry": "2027-04-10"}
        }
    },
    {
        "id": "CHC-MH-GAD-03",
        "name": "CHC Chamorshi Central",
        "type": "Community Health Centre",
        "district": "Gadchiroli",
        "state": "Maharashtra",
        "country": "India",
        "coordinates": {"lat": 19.9238, "lng": 79.9419},
        "coverage_population": 85000,
        "is_remote_access": False,
        "beds": {"total": 35, "occupied": 28, "icu_total": 4, "icu_occupied": 3, "maternity_total": 8, "maternity_occupied": 6},
        "staff": {"doctors_registered": 5, "doctors_on_duty": 4, "nurses_on_duty": 8, "pharmacists_on_duty": 2},
        "footfall": {"today": 260, "yesterday": 245, "seven_day_avg": 220, "surge_detected": False, "surge_reason": None},
        "inventory": {
            "med_antivenom": {"stock": 55, "daily_burn": 4, "batch_expiry": "2027-05-15"},
            "med_arv": {"stock": 70, "daily_burn": 5, "batch_expiry": "2027-06-20"},
            "med_insulin": {"stock": 80, "daily_burn": 6, "batch_expiry": "2027-03-30"},
            "med_paracetamol_iv": {"stock": 380, "daily_burn": 35, "batch_expiry": "2027-08-15"},
            "med_amox_clav": {"stock": 2100, "daily_burn": 120, "batch_expiry": "2027-09-01"},
            "med_ors": {"stock": 850, "daily_burn": 90, "batch_expiry": "2027-11-01"},
            "med_o2": {"stock": 18, "daily_burn": 4, "batch_expiry": "N/A"},
            "med_delivery_kit": {"stock": 60, "daily_burn": 5, "batch_expiry": "2028-05-01"},
            "med_malaria_rdt": {"stock": 320, "daily_burn": 25, "batch_expiry": "2027-04-15"},
            "med_doxycycline": {"stock": 1400, "daily_burn": 70, "batch_expiry": "2027-08-20"}
        }
    },
    {
        "id": "DWH-MH-WAR-01",
        "name": "District Medical Warehouse Wardha",
        "type": "District Medical Depot",
        "district": "Wardha",
        "state": "Maharashtra",
        "country": "India",
        "coordinates": {"lat": 20.7453, "lng": 78.6022},
        "coverage_population": 1300000,
        "is_remote_access": False,
        "beds": {"total": 120, "occupied": 98, "icu_total": 16, "icu_occupied": 13, "maternity_total": 25, "maternity_occupied": 20},
        "staff": {"doctors_registered": 18, "doctors_on_duty": 14, "nurses_on_duty": 32, "pharmacists_on_duty": 6},
        "footfall": {"today": 750, "yesterday": 710, "seven_day_avg": 690, "surge_detected": False, "surge_reason": None},
        "inventory": {
            "med_antivenom": {"stock": 240, "daily_burn": 5, "batch_expiry": "2027-08-20"},
            "med_arv": {"stock": 320, "daily_burn": 8, "batch_expiry": "2027-09-10"},
            "med_insulin": {"stock": 450, "daily_burn": 12, "batch_expiry": "2027-06-15"},
            "med_paracetamol_iv": {"stock": 2400, "daily_burn": 60, "batch_expiry": "2027-12-01"},
            "med_amox_clav": {"stock": 12500, "daily_burn": 250, "batch_expiry": "2027-11-20"},
            "med_ors": {"stock": 6500, "daily_burn": 180, "batch_expiry": "2028-02-15"},
            "med_o2": {"stock": 85, "daily_burn": 10, "batch_expiry": "N/A"},
            "med_delivery_kit": {"stock": 380, "daily_burn": 12, "batch_expiry": "2028-07-01"},
            "med_malaria_rdt": {"stock": 1900, "daily_burn": 40, "batch_expiry": "2027-08-10"},
            "med_doxycycline": {"stock": 7800, "daily_burn": 110, "batch_expiry": "2027-10-15"}
        }
    },
    {
        "id": "PHC-MH-WAR-02",
        "name": "PHC Seloo Rural",
        "type": "Primary Health Centre",
        "district": "Wardha",
        "state": "Maharashtra",
        "country": "India",
        "coordinates": {"lat": 20.8351, "lng": 78.7067},
        "coverage_population": 36000,
        "is_remote_access": False,
        "beds": {"total": 10, "occupied": 7, "icu_total": 0, "icu_occupied": 0, "maternity_total": 3, "maternity_occupied": 2},
        "staff": {"doctors_registered": 2, "doctors_on_duty": 2, "nurses_on_duty": 3, "pharmacists_on_duty": 1},
        "footfall": {"today": 92, "yesterday": 88, "seven_day_avg": 85, "surge_detected": False, "surge_reason": None},
        "inventory": {
            "med_antivenom": {"stock": 32, "daily_burn": 2, "batch_expiry": "2027-04-10"},
            "med_arv": {"stock": 25, "daily_burn": 2, "batch_expiry": "2027-05-18"},
            "med_insulin": {"stock": 40, "daily_burn": 3, "batch_expiry": "2027-02-28"},
            "med_paracetamol_iv": {"stock": 180, "daily_burn": 15, "batch_expiry": "2027-09-01"},
            "med_amox_clav": {"stock": 950, "daily_burn": 60, "batch_expiry": "2027-08-15"},
            "med_ors": {"stock": 420, "daily_burn": 30, "batch_expiry": "2027-10-01"},
            "med_o2": {"stock": 8, "daily_burn": 1, "batch_expiry": "N/A"},
            "med_delivery_kit": {"stock": 30, "daily_burn": 2, "batch_expiry": "2028-03-01"},
            "med_malaria_rdt": {"stock": 140, "daily_burn": 10, "batch_expiry": "2027-06-15"},
            "med_doxycycline": {"stock": 600, "daily_burn": 35, "batch_expiry": "2027-09-10"}
        }
    },
    {
        "id": "PHC-MH-WAR-03",
        "name": "PHC Deoli Agrarian",
        "type": "Primary Health Centre",
        "district": "Wardha",
        "state": "Maharashtra",
        "country": "India",
        "coordinates": {"lat": 20.6558, "lng": 78.4792},
        "coverage_population": 41000,
        "is_remote_access": False,
        "beds": {"total": 12, "occupied": 10, "icu_total": 0, "icu_occupied": 0, "maternity_total": 4, "maternity_occupied": 3},
        "staff": {"doctors_registered": 2, "doctors_on_duty": 1, "nurses_on_duty": 2, "pharmacists_on_duty": 1},
        "footfall": {"today": 125, "yesterday": 115, "seven_day_avg": 90, "surge_detected": True, "surge_reason": "Insecticide Exposure & Respiratory Influx"},
        "inventory": {
            "med_antivenom": {"stock": 20, "daily_burn": 2, "batch_expiry": "2027-03-12"},
            "med_arv": {"stock": 18, "daily_burn": 2, "batch_expiry": "2027-04-05"},
            "med_insulin": {"stock": 30, "daily_burn": 3, "batch_expiry": "2027-01-20"},
            "med_paracetamol_iv": {"stock": 110, "daily_burn": 20, "batch_expiry": "2027-07-15"},
            "med_amox_clav": {"stock": 600, "daily_burn": 70, "batch_expiry": "2027-07-20"},
            "med_ors": {"stock": 320, "daily_burn": 40, "batch_expiry": "2027-09-25"},
            "med_o2": {"stock": 4, "daily_burn": 2, "batch_expiry": "N/A"},
            "med_delivery_kit": {"stock": 25, "daily_burn": 2, "batch_expiry": "2028-02-15"},
            "med_malaria_rdt": {"stock": 110, "daily_burn": 12, "batch_expiry": "2027-05-10"},
            "med_doxycycline": {"stock": 450, "daily_burn": 40, "batch_expiry": "2027-08-15"}
        }
    },
    {
        "id": "PHC-UP-VAR-01",
        "name": "PHC Chiraigaon (Ganges Riverine)",
        "type": "Primary Health Centre",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "country": "India",
        "coordinates": {"lat": 25.3887, "lng": 83.0534},
        "coverage_population": 52000,
        "is_remote_access": False,
        "beds": {"total": 15, "occupied": 15, "icu_total": 0, "icu_occupied": 0, "maternity_total": 5, "maternity_occupied": 5},
        "staff": {"doctors_registered": 3, "doctors_on_duty": 2, "nurses_on_duty": 4, "pharmacists_on_duty": 1},
        "footfall": {"today": 230, "yesterday": 210, "seven_day_avg": 130, "surge_detected": True, "surge_reason": "Post-Monsoon Dengue Serotype Spike"},
        "inventory": {
            "med_antivenom": {"stock": 15, "daily_burn": 2, "batch_expiry": "2027-02-28"},
            "med_arv": {"stock": 12, "daily_burn": 3, "batch_expiry": "2027-03-15"},
            "med_insulin": {"stock": 22, "daily_burn": 4, "batch_expiry": "2027-01-10"},
            "med_paracetamol_iv": {"stock": 28, "daily_burn": 45, "batch_expiry": "2027-05-01"},
            "med_amox_clav": {"stock": 280, "daily_burn": 85, "batch_expiry": "2027-06-15"},
            "med_ors": {"stock": 90, "daily_burn": 75, "batch_expiry": "2027-08-20"},
            "med_o2": {"stock": 5, "daily_burn": 3, "batch_expiry": "N/A"},
            "med_delivery_kit": {"stock": 18, "daily_burn": 3, "batch_expiry": "2028-01-20"},
            "med_malaria_rdt": {"stock": 35, "daily_burn": 40, "batch_expiry": "2027-03-30"},
            "med_doxycycline": {"stock": 180, "daily_burn": 65, "batch_expiry": "2027-06-10"}
        }
    },
    {
        "id": "DWH-UP-VAR-02",
        "name": "Varanasi Regional Medical Store Depot",
        "type": "District Medical Depot",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "country": "India",
        "coordinates": {"lat": 25.3176, "lng": 82.9739},
        "coverage_population": 3600000,
        "is_remote_access": False,
        "beds": {"total": 250, "occupied": 210, "icu_total": 35, "icu_occupied": 31, "maternity_total": 40, "maternity_occupied": 35},
        "staff": {"doctors_registered": 42, "doctors_on_duty": 36, "nurses_on_duty": 80, "pharmacists_on_duty": 12},
        "footfall": {"today": 1450, "yesterday": 1410, "seven_day_avg": 1380, "surge_detected": False, "surge_reason": None},
        "inventory": {
            "med_antivenom": {"stock": 380, "daily_burn": 8, "batch_expiry": "2027-09-20"},
            "med_arv": {"stock": 460, "daily_burn": 12, "batch_expiry": "2027-10-15"},
            "med_insulin": {"stock": 850, "daily_burn": 20, "batch_expiry": "2027-08-10"},
            "med_paracetamol_iv": {"stock": 4200, "daily_burn": 110, "batch_expiry": "2028-01-10"},
            "med_amox_clav": {"stock": 18000, "daily_burn": 350, "batch_expiry": "2027-12-15"},
            "med_ors": {"stock": 9500, "daily_burn": 220, "batch_expiry": "2028-03-01"},
            "med_o2": {"stock": 140, "daily_burn": 15, "batch_expiry": "N/A"},
            "med_delivery_kit": {"stock": 650, "daily_burn": 18, "batch_expiry": "2028-08-20"},
            "med_malaria_rdt": {"stock": 3100, "daily_burn": 60, "batch_expiry": "2027-09-01"},
            "med_doxycycline": {"stock": 11000, "daily_burn": 150, "batch_expiry": "2027-11-10"}
        }
    },
    {
        "id": "PHC-KL-WAY-01",
        "name": "PHC Meppadi (Highland Landslide Risk)",
        "type": "Primary Health Centre",
        "district": "Wayanad",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 11.5511, "lng": 76.1264},
        "coverage_population": 29000,
        "is_remote_access": True,
        "beds": {"total": 16, "occupied": 14, "icu_total": 2, "icu_occupied": 2, "maternity_total": 4, "maternity_occupied": 3},
        "staff": {"doctors_registered": 3, "doctors_on_duty": 3, "nurses_on_duty": 5, "pharmacists_on_duty": 2},
        "footfall": {"today": 178, "yesterday": 165, "seven_day_avg": 110, "surge_detected": True, "surge_reason": "Flood-Related Trauma & Waterborne Triage"},
        "inventory": {
            "med_antivenom": {"stock": 18, "daily_burn": 3, "batch_expiry": "2027-04-12"},
            "med_arv": {"stock": 22, "daily_burn": 2, "batch_expiry": "2027-05-10"},
            "med_insulin": {"stock": 35, "daily_burn": 4, "batch_expiry": "2027-03-15"},
            "med_paracetamol_iv": {"stock": 65, "daily_burn": 28, "batch_expiry": "2027-07-15"},
            "med_amox_clav": {"stock": 510, "daily_burn": 80, "batch_expiry": "2027-08-01"},
            "med_ors": {"stock": 110, "daily_burn": 95, "batch_expiry": "2027-09-10"},
            "med_o2": {"stock": 6, "daily_burn": 3, "batch_expiry": "N/A"},
            "med_delivery_kit": {"stock": 24, "daily_burn": 3, "batch_expiry": "2028-04-15"},
            "med_malaria_rdt": {"stock": 90, "daily_burn": 15, "batch_expiry": "2027-05-20"},
            "med_doxycycline": {"stock": 520, "daily_burn": 70, "batch_expiry": "2027-08-15"}
        }
    },
    {
        "id": "PHC-MH-PUN-01",
        "name": "PHC Shirur Agro-Corridor",
        "type": "Primary Health Centre",
        "district": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "coordinates": {"lat": 18.8267, "lng": 74.3773},
        "coverage_population": 48000,
        "is_remote_access": False,
        "beds": {"total": 15, "occupied": 10, "icu_total": 0, "icu_occupied": 0, "maternity_total": 4, "maternity_occupied": 2},
        "staff": {"doctors_registered": 3, "doctors_on_duty": 2, "nurses_on_duty": 4, "pharmacists_on_duty": 1},
        "footfall": {"today": 130, "yesterday": 124, "seven_day_avg": 120, "surge_detected": False, "surge_reason": None},
        "inventory": {
            "med_antivenom": {"stock": 42, "daily_burn": 2, "batch_expiry": "2027-06-10"},
            "med_arv": {"stock": 35, "daily_burn": 3, "batch_expiry": "2027-07-15"},
            "med_insulin": {"stock": 60, "daily_burn": 4, "batch_expiry": "2027-05-20"},
            "med_paracetamol_iv": {"stock": 240, "daily_burn": 18, "batch_expiry": "2027-10-10"},
            "med_amox_clav": {"stock": 1100, "daily_burn": 75, "batch_expiry": "2027-09-15"},
            "med_ors": {"stock": 580, "daily_burn": 40, "batch_expiry": "2027-12-01"},
            "med_o2": {"stock": 10, "daily_burn": 1, "batch_expiry": "N/A"},
            "med_delivery_kit": {"stock": 45, "daily_burn": 3, "batch_expiry": "2028-05-15"},
            "med_malaria_rdt": {"stock": 220, "daily_burn": 15, "batch_expiry": "2027-07-20"},
            "med_doxycycline": {"stock": 850, "daily_burn": 45, "batch_expiry": "2027-10-05"}
        }
    }
]

# BRICS Federated Nodes Registry
BRICS_NODES: List[Dict[str, Any]] = [
    {
        "country_code": "IND",
        "country_name": "India",
        "grid_name": "ArogyaFederate India Mesh",
        "health_authority": "Ministry of Health & Family Welfare (MoHFW)",
        "active_phc_nodes": 28412,
        "population_monitored": "1.42 Billion",
        "last_federated_round": 142,
        "differential_privacy_budget_spent": 0.42,
        "local_loss": 0.184,
        "shared_outbreak_vector": "DENV-2 Dengue & Cholera O1 Spikes",
        "status": "Active & Syncing"
    },
    {
        "country_code": "BRA",
        "country_name": "Brazil",
        "grid_name": "SUS Rede Conectada",
        "health_authority": "Ministério da Saúde (SUS)",
        "active_phc_nodes": 19480,
        "population_monitored": "215 Million",
        "last_federated_round": 142,
        "differential_privacy_budget_spent": 0.39,
        "local_loss": 0.198,
        "shared_outbreak_vector": "Dengue Hyper-Endemic Surge (Minas Gerais & Amazonas)",
        "status": "Active & Syncing"
    },
    {
        "country_code": "ZAF",
        "country_name": "South Africa",
        "grid_name": "NHI Resilient Supply Grid",
        "health_authority": "National Department of Health (NDoH)",
        "active_phc_nodes": 4210,
        "population_monitored": "60 Million",
        "last_federated_round": 142,
        "differential_privacy_budget_spent": 0.35,
        "local_loss": 0.215,
        "shared_outbreak_vector": "Seasonal Respiratory & Rural Antivenom Buffer Deficit",
        "status": "Active & Syncing"
    },
    {
        "country_code": "EGY",
        "country_name": "Egypt",
        "grid_name": "100 Million Healthy Lives Grid",
        "health_authority": "Ministry of Health and Population",
        "active_phc_nodes": 5420,
        "population_monitored": "110 Million",
        "last_federated_round": 141,
        "differential_privacy_budget_spent": 0.38,
        "local_loss": 0.207,
        "shared_outbreak_vector": "Pediatric Gastrointestinal & Insulin Cold-Chain Optimization",
        "status": "Active & Syncing"
    }
]

def calculate_haversine_distance_km(coord1: Dict[str, float], coord2: Dict[str, float]) -> float:
    """Calculate distance in kilometers between two GPS coordinates."""
    lat1, lon1 = math.radians(coord1["lat"]), math.radians(coord1["lng"])
    lat2, lon2 = math.radians(coord2["lat"]), math.radians(coord2["lng"])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371.0 # Earth radius in km
    return round(c * r, 1)
