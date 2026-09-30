"""
PulseGrid BRICS - Cross-District Resource Redistribution Optimizer
Calculates priority-weighted reallocations from surplus depots/PHCs to deficit PHCs
minimizing transit time, preserving donor buffers, and handling cold-chain requirements.
"""

from typing import List, Dict, Any
from .mock_data import FACILITIES_SEED, MEDICINE_CATALOG, calculate_haversine_distance_km

class ResourceRedistributionOptimizer:
    def __init__(self, facilities: List[Dict[str, Any]] = None):
        self.facilities = facilities or FACILITIES_SEED
        self.med_catalog_map = {m["id"]: m for m in MEDICINE_CATALOG}

    def evaluate_inventory_health(self) -> Dict[str, Any]:
        """Calculates runway days and critical shortage flags for all facilities."""
        summary = {
            "total_facilities": len(self.facilities),
            "critical_stockouts_count": 0,
            "warning_stockouts_count": 0,
            "healthy_facilities_count": 0,
            "facility_reports": []
        }

        for fac in self.facilities:
            crit_count = 0
            warn_count = 0
            med_reports = []

            for med_id, inv in fac["inventory"].items():
                meta = self.med_catalog_map.get(med_id, {})
                burn = inv["daily_burn"]
                stock = inv["stock"]
                runway_days = round(stock / max(burn, 0.1), 1)
                crit_threshold = meta.get("critical_threshold_days", 4)

                status = "HEALTHY"
                if runway_days <= crit_threshold:
                    status = "CRITICAL"
                    crit_count += 1
                elif runway_days <= (crit_threshold * 2):
                    status = "WARNING"
                    warn_count += 1

                med_reports.append({
                    "med_id": med_id,
                    "med_name": meta.get("name", med_id),
                    "category": meta.get("category", "General"),
                    "stock": stock,
                    "daily_burn": burn,
                    "runway_days": runway_days,
                    "unit": meta.get("unit", "units"),
                    "status": status,
                    "cold_chain": meta.get("cold_chain", False)
                })

            if crit_count > 0:
                summary["critical_stockouts_count"] += 1
                fac_status = "CRITICAL"
            elif warn_count > 0:
                summary["warning_stockouts_count"] += 1
                fac_status = "WARNING"
            else:
                summary["healthy_facilities_count"] += 1
                fac_status = "HEALTHY"

            summary["facility_reports"].append({
                "facility_id": fac["id"],
                "facility_name": fac["name"],
                "facility_type": fac["type"],
                "district": fac["district"],
                "state": fac["state"],
                "coordinates": fac["coordinates"],
                "footfall": fac["footfall"],
                "beds": fac["beds"],
                "staff": fac["staff"],
                "overall_status": fac_status,
                "critical_medicine_count": crit_count,
                "medicines": med_reports
            })

        return summary

    def generate_redistribution_plan(self) -> List[Dict[str, Any]]:
        """
        Finds deficit facilities (runway <= critical_threshold) and pairs them with
        the closest surplus facility (runway > 14 days) to generate actionable dispatch manifests.
        """
        recommendations = []

        # Find all deficit points
        for target in self.facilities:
            for med_id, inv in target["inventory"].items():
                meta = self.med_catalog_map.get(med_id, {})
                burn = inv["daily_burn"]
                stock = inv["stock"]
                runway = stock / max(burn, 0.1)
                crit_threshold = meta.get("critical_threshold_days", 4)

                if runway <= crit_threshold:
                    # Target needs stock! Calculate target needed for 7 days safe runway
                    desired_target_stock = burn * 8
                    deficit_amount = int(max(desired_target_stock - stock, burn * 4))

                    # Look for best donor
                    best_donor = None
                    best_score = -999999.0
                    best_distance = 0.0
                    transfer_qty = 0

                    for donor in self.facilities:
                        if donor["id"] == target["id"]:
                            continue

                        donor_inv = donor["inventory"].get(med_id)
                        if not donor_inv:
                            continue

                        donor_stock = donor_inv["stock"]
                        donor_burn = donor_inv["daily_burn"]
                        donor_runway = donor_stock / max(donor_burn, 0.1)

                        # Donor must retain at least 10 days of runway
                        min_retained_stock = donor_burn * 10
                        available_surplus = int(donor_stock - min_retained_stock)

                        if available_surplus > 0:
                            dist_km = calculate_haversine_distance_km(donor["coordinates"], target["coordinates"])
                            # Prefer donors in same state / closer distance / district warehouses
                            is_warehouse_boost = 50.0 if "Depot" in donor["type"] or "Warehouse" in donor["name"] else 0.0
                            # Priority Score: high surplus, low distance, warehouse preference
                            score = (available_surplus / (burn + 1)) * 10 - (dist_km * 0.4) + is_warehouse_boost

                            if score > best_score:
                                best_score = score
                                best_donor = donor
                                best_distance = dist_km
                                transfer_qty = min(deficit_amount, available_surplus)

                    if best_donor and transfer_qty > 0:
                        # Transport vehicle selection
                        cold_chain = meta.get("cold_chain", False)
                        if cold_chain:
                            vehicle = "Refrigerated Cryo-Logistics Van (2°C - 8°C Active Chiller)"
                        elif runway <= 1.5:
                            vehicle = "Rapid Response Emergency Ambulance (Siren Escort)"
                        else:
                            vehicle = "District Medical Logistics Cruiser"

                        # Estimate transit time (hours)
                        speed_kmh = 45.0 if target.get("is_remote_access") else 60.0
                        est_transit_hours = round(best_distance / speed_kmh, 1)

                        post_transfer_runway = round((stock + transfer_qty) / max(burn, 0.1), 1)

                        recommendations.append({
                            "id": f"REC-{target['id'][-6:]}-{med_id[:6].upper()}",
                            "priority": "HIGH" if runway <= 1.5 else "MEDIUM",
                            "recipient": {
                                "id": target["id"],
                                "name": target["name"],
                                "district": target["district"],
                                "coordinates": target["coordinates"],
                                "current_runway_days": round(runway, 1),
                                "projected_runway_days": post_transfer_runway,
                                "surge_detected": target["footfall"]["surge_detected"],
                                "surge_reason": target["footfall"]["surge_reason"]
                            },
                            "donor": {
                                "id": best_donor["id"],
                                "name": best_donor["name"],
                                "district": best_donor["district"],
                                "coordinates": best_donor["coordinates"],
                                "surplus_available": best_donor["inventory"][med_id]["stock"]
                            },
                            "medicine": {
                                "id": med_id,
                                "name": meta.get("name", med_id),
                                "category": meta.get("category", "General"),
                                "unit": meta.get("unit", "units"),
                                "cold_chain": cold_chain
                            },
                            "transfer_quantity": transfer_qty,
                            "distance_km": best_distance,
                            "estimated_transit_hours": est_transit_hours,
                            "recommended_transport": vehicle,
                            "status": "PROPOSED",
                            "carbon_footprint_kg_co2": round(best_distance * 0.18, 1)
                        })

        # Sort recommendations by highest urgency
        recommendations.sort(key=lambda r: (r["priority"] == "HIGH", -r["transfer_quantity"]), reverse=True)
        return recommendations
