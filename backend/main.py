from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import psycopg2
import os
from datetime import datetime
from typing import Optional

app = FastAPI()

# Database connection configuration for Docker environment [cite: 33, 592]
def get_db_conn():
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("DB_NAME", "amaorm"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "Revanth")
        )
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None

# Automated Fee Calculation Logic [cite: 24, 38]
def calculate_amaorm_fee(width, height, is_violation=False):
    base_rate = 500.0  # Base rate per square unit [cite: 285]
    area = width * height
    # Penalty multiplier for unauthorized or mismatched structures [cite: 226, 285]
    multiplier = 2.0 if is_violation else 1.0 
    return area * base_rate * multiplier

# --- MONITORING & ENFORCEMENT ENDPOINT ---
@app.get("/verify")
def verify_hoarding(lat: float, lon: float, detected_w: float = 0, detected_h: float = 0, qr_code: Optional[str] = None):
    """
    Main Verification Loop: Cross-references AI detections with GIS records [cite: 43, 137, 627]
    """
    conn = get_db_conn()
    if not conn: raise HTTPException(status_code=500, detail="DB Connection Failed")
    cur = conn.cursor()
    
    # 5-Meter Tolerance Spatial Query to handle GPS drift [cite: 144, 162, 604]
    query = """
    SELECT agency_name, license_number, expiry_date, stability_cert_expiry, dimensions_width, dimensions_height
    FROM legal_hoardings
    WHERE ST_DWithin(geom, ST_SetSRID(ST_Point(%s, %s), 4326), 0.00005);
    """
    cur.execute(query, (lon, lat))
    result = cur.fetchone()
    
    # Case A: Unauthorized Structure (No record found) [cite: 47, 146, 635]
    if not result:
        fine = calculate_amaorm_fee(detected_w, detected_h, is_violation=True)
        return {
            "status": "ILLEGAL",
            "type": "Unauthorized Structure",
            "fine_amount": fine,
            "action": "Automated Notice Generation Triggered"
        }

    agency, lic_num, expiry, stability, reg_w, reg_h = result
    today = datetime.now().date()

    # Case B: Compliance Checks (Expiry, Size, and QR) [cite: 46, 115, 637]
    if qr_code and qr_code != lic_num:
        return {"status": "VIOLATION", "type": "License/QR Mismatch", "license": lic_num}
    
    if expiry < today:
        return {"status": "VIOLATION", "type": "Expired Permit", "license": lic_num}
        
    if stability < today:
        return {"status": "VIOLATION", "type": "Stability Certificate Expired", "license": lic_num}

    # Under-reporting detection (10% tolerance for physical measurement) [cite: 15, 224, 637]
    if detected_w > (reg_w * 1.1) or detected_h > (reg_h * 1.1):
        return {
            "status": "VIOLATION", 
            "type": "Size Mismatch (Under-reporting)", 
            "license": lic_num,
            "penalty": calculate_amaorm_fee(detected_w - reg_w, detected_h - reg_h)
        }

    return {"status": "LEGAL", "agency": agency, "license": lic_num}

# --- APPLICANT PORTAL ENDPOINT ---
@app.post("/submit-application")
async def submit_application(
    agency: str = Form(...), 
    license_id: str = Form(...), 
    lat: float = Form(...), 
    lon: float = Form(...),
    stability_cert: UploadFile = File(...),
    site_image: UploadFile = File(...)
):
    """
    Handles new data uploads from agencies/owners [cite: 24, 41, 231]
    """
    conn = get_db_conn()
    cur = conn.cursor()
    
    # Automated document verification placeholder [cite: 24]
    # In production, save files to /app/uploads and update PostGIS
    try:
        query = """
        INSERT INTO legal_hoardings (agency_name, license_number, geom, license_status)
        VALUES (%s, %s, ST_SetSRID(ST_Point(%s, %s), 4326), FALSE);
        """
        cur.execute(query, (agency, license_id, lon, lat))
        conn.commit()
        return {"message": "Application received. Pending AI Document Verification."}
    except Exception as e:
        return {"error": str(e)}