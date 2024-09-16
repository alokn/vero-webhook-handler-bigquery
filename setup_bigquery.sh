#!/bin/bash

# Function to handle errors
handle_error() {
    echo "Error: $1" >&2
    exit 1
}

# Set variables
PROJECT_ID="<YOUR_PROJECT_ID>"
DATASET="<YOUR_DATASET>"
TABLE="<YOUR_TABLE>"

dataset_name="$PROJECT_ID:$DATASET"
full_table_name="$PROJECT_ID:$DATASET.$TABLE"

# Create the dataset
echo "Creating dataset ${DATASET}..."
bq --location=US mk --dataset \
    --description "Dataset for Vero webhook logs" \
    "$dataset_name" || handle_error "Failed to create dataset"

# Create the table using the schema file
echo "Creating table ${TABLE}..."
bq mk --table \
    --description "Table for Vero webhook logs" \
    "$full_table_name" \
    schema.json || handle_error "Failed to create table"

echo "BigQuery dataset and table created successfully."