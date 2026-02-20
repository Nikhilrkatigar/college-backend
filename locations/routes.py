# locations/routes.py
from fastapi import APIRouter
import json
from pathlib import Path


router = APIRouter(prefix="/locations", tags=["Locations"])

# Load India JSON once (FAST + OFFLINE)
# Load from data folder (one level up from locations)
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "india_locations.json"

if not DATA_PATH.exists():
    raise FileNotFoundError(f"india_locations.json not found at {DATA_PATH}")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    INDIA = json.load(f)

# ====================================
# GET REGIONS
# ====================================
@router.get("/regions")
def get_regions():
    """Get all regions (North, South, East, West, etc.)"""
    return [k for k in INDIA.keys() if k != "metadata"]

# ====================================
# GET STATES BY REGION
# ====================================
@router.get("/states")
def get_states(region: str):
    """Get all states in a region"""
    return list(INDIA.get(region, {}).keys()) if region in INDIA else []

# ====================================
# GET DISTRICTS BY STATE
# ====================================
@router.get("/districts")
def get_districts(region: str, state: str):
    """Get all districts in a state"""
    state_data = INDIA.get(region, {}).get(state, {})
    if isinstance(state_data, dict) and "districts" in state_data:
        return list(state_data["districts"].keys())
    return []

# ====================================
# GET CITIES BY DISTRICT
# ====================================
@router.get("/cities")
def get_cities(region: str, state: str, district: str):
    """Get all cities in a district"""
    state_data = INDIA.get(region, {}).get(state, {})
    if isinstance(state_data, dict) and "districts" in state_data:
        return state_data["districts"].get(district, [])
    return []

