CREATE TABLE detections (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    frame BYTEA,
    has_ppe BOOLEAN,
    details JSONB
);
