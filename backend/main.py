from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import psycopg2
import os
from datetime import datetime
from typing import Optional
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = FastAPI()

# --- DATABASE CONNECTION ---
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

# --- REPORT GENERATION LOGIC ---
def generate_violation_report(lat, lon, violation_type, license_num="N/A", fine=0.0):
    """
    Generates a PDF legal notice for the detected violation.
    """
    os.makedirs('reports', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"reports/NOTICE_{violation_type.replace(' ', '_')}_{timestamp}.pdf"
    
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Header & Styling
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "A-MAORM: AUTOMATED ENFORCEMENT NOTICE")
    c.line(50, height - 60, 550, height - 60)

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Date Issued: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 120, f"Violation Type: {violation_type}")
    c.drawString(50, height - 140, f"GPS Coordinates: {lat}, {lon}")
    c.drawString(50, height - 160, f"Associated License: {license_num}")

    # Penalty Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 200, f"Total Calculated Fine: ₹{fine:,.2f}")

    # Legal Text
    c.setFont("Helvetica-Oblique", 10)
    text = [
        "This notice was generated automatically by the A-MAORM AI Surveillance System.",
        "The structure detected at the above coordinates was found to be in non-compliance",
        "with municipal outdoor advertising regulations. Please contact the municipal",
        "office within 48 hours to resolve this violation."
    ]
    y_pos = height - 250
    for line in text:
        c.drawString(50, y_pos, line)
        y_pos -= 15

    c.save()
    return file_name

# --- FEE CALCULATION ---
def calculate_amaorm_fee(width, height, is_violation=False):
    base_rate = 500.0  
    area = width * height
    multiplier = 2.0 if is_violation else 1.0 
    return area * base_rate * multiplier

# --- MONITORING & ENFORCEMENT ENDPOINT ---
@app.get("/verify")
def verify_hoarding(lat: float, lon: float, detected_w: float = 0, detected_h: float = 0, qr_code: Optional[str] = None):
    conn = get_db_conn()
    if not conn: raise HTTPException(status_code=500, detail="DB Connection Failed")
    cur = conn.cursor()
    
    # 5-Meter Tolerance Spatial Query
    query = """
    SELECT agency_name, license_number, expiry_date, stability_cert_expiry, dimensions_width, dimensions_height
    FROM legal_hoardings
    WHERE ST_DWithin(geom, ST_SetSRID(ST_Point(%s, %s), 4326), 0.00005);
    """
    cur.execute(query, (lon, lat))
    result = cur.fetchone()
    
    # Case A: Unauthorized Structure
    if not result:
        fine = calculate_amaorm_fee(detected_w, detected_h, is_violation=True)
        report = generate_violation_report(lat, lon, "Unauthorized Structure", fine=fine)
        return {
            "status": "ILLEGAL",
            "type": "Unauthorized Structure",
            "fine_amount": fine,
            "notice_pdf": report
        }

    agency, lic_num, expiry, stability, reg_w, reg_h = result
    today = datetime.now().date()

    # Case B: Compliance Checks
    violation = None
    if qr_code and qr_code != lic_num:
        violation = "License/QR Mismatch"
    elif expiry < today:
        violation = "Expired Permit"
    elif stability < today:
        violation = "Stability Certificate Expired"
    elif detected_w > (reg_w * 1.1) or detected_h > (reg_h * 1.1):
        violation = "Size Mismatch (Under-reporting)"

    if violation:
        fine = calculate_amaorm_fee(detected_w, detected_h, is_violation=True)
        report = generate_violation_report(lat, lon, violation, license_num=lic_num, fine=fine)
        return {
            "status": "VIOLATION",
            "type": violation,
            "license": lic_num,
            "notice_pdf": report
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
    conn = get_db_conn()
    cur = conn.cursor()
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