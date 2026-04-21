CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE legal_hoardings (
    id SERIAL PRIMARY KEY,
    agency_name VARCHAR(255),
    license_number VARCHAR(100) UNIQUE,
    expiry_date DATE,
    geom GEOMETRY(Point, 4326),
    dimensions_width FLOAT,
    dimensions_height FLOAT,
    stability_cert_expiry DATE
);

CREATE INDEX hoarding_geo_idx ON legal_hoardings USING GIST (geom);

INSERT INTO legal_hoardings (agency_name, license_number, expiry_date, geom, dimensions_width, dimensions_height, stability_cert_expiry)
VALUES ('Alpha Media', 'LIC-2026-001', '2026-12-31', ST_SetSRID(ST_Point(77.5946, 12.9716), 4326), 10.0, 5.0, '2026-11-01');