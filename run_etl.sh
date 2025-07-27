#!/bin/bash

# Step 1: Start persistent services like PostgreSQL
docker-compose -f docker/docker-compose.yml up -d postgres

# Step 2: Build and run ETL job
docker build -t crypto-etl -f docker/etl/Dockerfile .
docker run --rm --network="host" crypto-etl

# Optional: Run tests or data checks here

# Step 3: (DO NOT STOP POSTGRES)
echo "ETL completed. PostgreSQL remains running..."
