"""
PulseGrid BRICS - Main FastAPI Application
Exposes REST APIs for Primary Health Centre telemetry, cross-district redistribution,
demand forecasting, BRICS federated learning, and Gemini 3.8 Flash triage copilot.
"""

import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from .mock_data import FACILITIES_SEED, MEDICINE_CATALOG, BRICS_NODES
from .optimizer import ResourceRedistributionOptimizer
from .federated_engine import BRICSFederatedMeshEngine
from .forecast_engine import generate_forecast_curves
from .gemini_service import GeminiTriageService

app = FastAPI(
    title="PulseGrid BRICS - Federated National Health & Supply Intelligence API",
    description="Real-time PHC visibility, automated cross-district redistribution, and BRICS federated learning platform.",
    version="1.0.0"
)

# Enable CORS for cross-origin or local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Services
optimizer = ResourceRedistributionOptimizer(FACILITIES_SEED)
federated_engine = BRICSFederatedMeshEngine()
gemini_service = GeminiTriageService()

# Dispatched manifests tracking store
dispatched_manifests = []

class TriageRequest(BaseModel):
    prompt: str
    facility_id: Optional[str] = None

class DispatchRequest(BaseModel):
    manifest_id: str
    approver_name: str
    notes: Optional[str] = "Approved by District Health Operations Officer"

@app.get("/api/health")
def health_check():
    return {
        "status": "OPERATIONAL",
        "service": "PulseGrid BRICS National Engine",
        "model": gemini_service.model_name,
        "genai_live": gemini_service.client is not None,
        "federated_nodes_active": len(BRICS_NODES),
        "phcs_tracked": len(FACILITIES_SEED)
    }

@app.get("/api/phcs")
def get_phc_network():
    """Returns the full network status including inventory, beds, staff, and surges."""
    return optimizer.evaluate_inventory_health()

@app.get("/api/inventory/critical")
def get_critical_inventory():
    """Returns facilities facing critical stock-out within 4 days."""
    health_data = optimizer.evaluate_inventory_health()
    critical_facilities = [
        f for f in health_data["facility_reports"]
        if f["overall_status"] == "CRITICAL"
    ]
    return {
        "count": len(critical_facilities),
        "critical_facilities": critical_facilities
    }

@app.get("/api/redistribution/plan")
def get_redistribution_plan():
    """Generates and returns optimized cross-district supply reallocation manifests."""
    plan = optimizer.generate_redistribution_plan()
    return {
        "total_proposals": len(plan),
        "plan": plan,
        "dispatched_manifests": dispatched_manifests
    }

@app.post("/api/redistribution/dispatch")
def approve_dispatch(req: DispatchRequest):
    """Executes authorization of an emergency cross-district transfer manifest."""
    plan = optimizer.generate_redistribution_plan()
    target_item = next((p for p in plan if p["id"] == req.manifest_id), None)

    if not target_item:
        # Fallback if already approved or mock ID
        manifest_record = {
            "manifest_id": req.manifest_id,
            "status": "DISPATCHED",
            "approver": req.approver_name,
            "notes": req.notes,
            "timestamp": "Just now",
            "eta": "2.4 hours"
        }
    else:
        target_item["status"] = "DISPATCHED"
        manifest_record = {
            "manifest_id": target_item["id"],
            "medicine": target_item["medicine"]["name"],
            "quantity": target_item["transfer_quantity"],
            "donor": target_item["donor"]["name"],
            "recipient": target_item["recipient"]["name"],
            "vehicle": target_item["recommended_transport"],
            "approver": req.approver_name,
            "status": "IN_TRANSIT",
            "timestamp": "Just now",
            "eta": f"{target_item['estimated_transit_hours']} hours"
        }

    dispatched_manifests.append(manifest_record)
    return {
        "success": True,
        "message": f"Transfer manifest {req.manifest_id} officially authorized and dispatched.",
        "record": manifest_record
    }

@app.get("/api/forecast")
def get_demand_forecast(facility_id: str = "PHC-MH-GAD-01"):
    """Returns 7-day predictive curves for critical emergency supplies."""
    return generate_forecast_curves(facility_id)

@app.get("/api/federated/mesh")
def get_federated_mesh():
    """Returns BRICS federated learning network telemetry and cross-border insights."""
    return federated_engine.get_mesh_status()

@app.post("/api/federated/round")
def trigger_federated_round():
    """Triggers an iterative federated learning training round."""
    return federated_engine.trigger_federated_round()

@app.post("/api/gemini/triage")
def run_gemini_triage(req: TriageRequest):
    """Executes conversational or automated triage via Gemini 3.8 Flash."""
    context = None
    if req.facility_id:
        context = next((f for f in FACILITIES_SEED if f["id"] == req.facility_id), None)
    else:
        context = {
            "total_phcs": len(FACILITIES_SEED),
            "critical_stockouts": [f["name"] for f in FACILITIES_SEED if f["footfall"]["surge_detected"]],
            "active_brics_round": federated_engine.current_round
        }

    result = gemini_service.analyze_incident_or_query(req.prompt, context)
    return result

# Path to static frontend directory
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

    @app.get("/pitch")
    def serve_pitch():
        return FileResponse(os.path.join(FRONTEND_DIR, "pitch.html"))
