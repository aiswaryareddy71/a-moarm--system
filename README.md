# A-MAORM: AI-Driven Municipal Advertising Oversight & Revenue Management

[cite_start]A-MAORM is a 2026-generation Smart City framework designed to automate the lifecycle of outdoor advertising management[cite: 2, 53]. [cite_start]By integrating high-speed AI surveillance with spatial GIS databases, the system eliminates manual inspection gaps, captures 100% of illegal revenue leakage, and ensures urban safety[cite: 3, 28, 30].

## 🏗️ System Architecture
[cite_start]The system operates as a fully integrated, automated enforcement loop[cite: 6, 207]:

1.  [cite_start]**AI Detection (The "Eyes")**: Uses YOLO26 (NMS-free architecture) for real-time identification of Unipoles, Billboards, and Gantries at speeds up to 60 km/h[cite: 54, 56, 85].
2.  [cite_start]**Spatial Verification (The "Brain")**: A PostGIS-powered backend cross-references GPS coordinates against a legal registry using a 5-meter tolerance buffer[cite: 18, 144, 162].
3.  [cite_start]**Automated Fee Engine**: Calculates dynamic fees based on physical dimensions (width/height) and zoning bylaws without human bias[cite: 24, 38].
4.  [cite_start]**Enforcement Dashboard**: Provides Ward Officers with real-time "Violation Alerts" and auto-generates legally binding PDF Notices of Violation (NoV)[cite: 41, 180, 217].

## 🚀 Key Technical Benchmarks
* [cite_start]**Processing Latency**: 43% faster than 2024 models, processing high-resolution frames in ~2.5ms[cite: 59, 84, 131].
* [cite_start]**Detection Accuracy**: Targeted >95% precision using Small-Target-Aware Labeling (STAL) for reading license IDs and QR codes[cite: 111, 263, 297].
* [cite_start]**Edge Capability**: Privacy-at-source processing ensures facial and private plate blurring happens directly on the vehicle hardware[cite: 68, 564, 565].

## 📂 Repository Structure
* [cite_start]`/backend`: FastAPI server handling spatial queries, fee calculation, and PDF generation[cite: 639, 680].
* [cite_start]`/db`: PostGIS database schema and initialization scripts[cite: 103, 591, 667].
* [cite_start]`/ai_engine`: YOLO26 inference scripts and STAL optimization protocols[cite: 121, 258, 445].
* [cite_start]`/dashboard`: Map-first monitoring interface for municipal ward officers[cite: 182, 186].
* [cite_start]`/reports`: Storage for AI-generated legal evidence and violation notices[cite: 219, 233].

## 🛠️ Deployment Instructions
1.  **Clone the Repo**: `git clone https://github.com/your-username/a-maorm-system.git`
2.  **Configure Environment**: Add your `NGROK_TOKEN` and `MAPBOX_TOKEN` to the `.env` file.
3.  [cite_start]**Launch Infrastructure**: Run `docker-compose up --build` to start the PostGIS DB and API[cite: 33, 285].
4.  [cite_start]**Start Survey**: Run `python ai_engine/survey_sim.py` to begin real-time city scanning[cite: 703].

## ⚖️ Legal & Privacy
[cite_start]The system adheres to 2026 Digital Privacy Acts, employing automated Gaussian blurring for non-commercial PII (Personally Identifiable Information) and NTP time-stamping for irrefutable legal evidence[cite: 236, 301, 566].