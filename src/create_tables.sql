CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(50),
    timestamp TIMESTAMP, 
    frame BYTEA,
    detected_ppe BOOLEAN,
    details JSONB
);