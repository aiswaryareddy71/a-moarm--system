from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_violation_report(lat, lon, image_path=None):
    # Ensure reports folder exists
    os.makedirs('reports', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"reports/VIOLATION_{timestamp}.pdf"
    
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "A-MAORM: ILLEGAL HOARDING DETECTION NOTICE")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 100, f"Location Coordinates: {lat}, {lon}")
    c.drawString(50, height - 120, "Status: UNAUTHORIZED / NO LICENSE FOUND")

    # Body
    c.line(50, height - 130, 550, height - 130)
    c.drawString(50, height - 160, "This hoarding has been flagged by the automated survey vehicle.")
    c.drawString(50, height - 180, "No matching record exists within the municipal database (PostGIS).")

    # If your AI captures an image, we can embed it here
    if image_path and os.path.exists(image_path):
        c.drawImage(image_path, 50, height - 400, width=300, preserveAspectRatio=True)
        c.drawString(50, height - 420, "Fig 1: Photographic evidence captured by AI Engine.")

    c.save()
    print(f"✅ Report generated: {file_name}")
    return file_name